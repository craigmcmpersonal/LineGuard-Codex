import json
import uuid
from typing import Any, ClassVar, Iterator

from azure.core import MatchConditions
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError
from azure.core.paging import ItemPaged
from azure.storage.blob import ContainerClient, BlobServiceClient, BlobClient, FilteredBlob, BlobProperties

from develop import constants
from develop.monitoring.logger import Logger
from develop.session.base_session_store import BaseSessionStore
from develop.session.session import Session
from develop.session.user import User


class AzureStorageSessionStore(BaseSessionStore):
    _TAG_NAME_IDENTIFIER: ClassVar[str] = "id"
    _TAG_NAME_USER_IDENTIFIER: ClassVar[str] = "userid"

    def __init__(self, connection_string: str):
        container_name: str = "sessions"
        self._container_client: ContainerClient = BlobServiceClient.from_connection_string(
            connection_string
        ).get_container_client(
            container_name
        )
        if not self._container_client.exists():
            try:
                self._container_client.create_container()
            except ResourceExistsError as exception:
                Logger().debug(
                    exception
                )

    def create(self, user: User) -> Session:
        unique_identifier: uuid.UUID = uuid.uuid4()
        session_identifier: str = str(
            unique_identifier
        )
        session: Session = Session(
            user=user,
            identifier=session_identifier
        )
        session.on_creation()
        _, result = self.store(
            session=session
        )
        return result

    def delete(self, session_identifier: str):
        try:
           self._container_client.delete_blob(
                blob=session_identifier
           )
        except ResourceNotFoundError:
            pass

    def enumerate(self) -> Iterator[Session]:
        pages: ItemPaged[BlobProperties] = self._container_client.list_blobs()
        for blob in pages:
            blob: BlobProperties
            Logger().info(
                f"{blob.name} {blob.last_modified}"
            )
            if (session := self.try_get(
                session_identifier=blob.name
            )) is not None:
                yield session

    def find(self, user: User) -> list[Session]:
        filter_template: str = "\"{tag}\"='{value}'"
        filter_: str = filter_template.format(
            tag=self._TAG_NAME_USER_IDENTIFIER,
            value=user.identifier
        )
        Logger().info(
            filter_
        )
        pages: ItemPaged[FilteredBlob] = self._container_client.find_blobs_by_tags(
            filter_
        )
        results: list[Session] = []
        for blob in pages:
            blob: FilteredBlob
            Logger().info(
                blob.name
            )
            session: Session|None = self.try_get(
                session_identifier=blob.name
            )
            if session:
                results.append(session)
        return results

    def store(self, session: Session, etag: str|None = None) -> tuple[str, Session]:
        etag_key: str = "etag"
        session.on_update()
        bytes_: bytes = session.model_dump_json().encode(
            constants.ENCODING_JSON
        )
        tags: dict[str, Any] = {
            self._TAG_NAME_IDENTIFIER: session.identifier,
            self._TAG_NAME_USER_IDENTIFIER: session.user.identifier
        }
        client: BlobClient = self._container_client.get_blob_client(
            blob=session.identifier
        )
        properties: dict[str, Any] = client.upload_blob(
            data=bytes_,
            tags=tags,
            overwrite=True,
            etag=etag,
            match_condition=MatchConditions.IfNotModified
        ) if etag else client.upload_blob(
            data=bytes_,
            tags=tags,
            overwrite=True
        )
        new_etag: str = properties[etag_key]
        return new_etag, session

    def try_get(self, session_identifier: str) -> Session|None:
        try:
            characters: str = self._container_client.get_blob_client(
                blob=session_identifier
            ).download_blob(
                encoding=constants.ENCODING_JSON
            ).readall()
            json_: dict[str, Any] = json.loads(
                characters
            )
            result: Session = Session(
                data=json_
            )
            result.on_retrieval()
            return result
        except ResourceNotFoundError:
            return None
