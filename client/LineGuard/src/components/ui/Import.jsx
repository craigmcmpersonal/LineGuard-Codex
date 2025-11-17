import { useState } from "react"
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogDescription,
    DialogFooter,
    DialogClose,
} from "@/components/ui/dialog"

import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Upload, FileText, Link as LinkIcon } from "lucide-react"


export const Import = ({state, dispatchState, reference, open, onOpenChange, onImport, className }) => {
    const [pastedText, setPastedText] = useState("")
    const [file, setFile] = useState(null)

    const handleImport = () => {
        const payload = {
            text: pastedText,
            file: file,
        }
        onImport?.(payload)
        onOpenChange(false)
    }

    return (
        <Dialog open={open} onOpenChange={onOpenChange}>
            <DialogContent className="max-w-lg">
                <DialogHeader>
                    <DialogTitle>Import Your Bets</DialogTitle>
                    <DialogDescription>
                        Choose how you'd like to bring bets into your Hedging Assistant.
                    </DialogDescription>
                </DialogHeader>


                {/* ====== PASTE BET TEXT ====== */}
                <div className="space-y-3">
                    <h3 className="font-medium flex items-center gap-2">
                        <FileText className="w-4 h-4 text-primary" />
                        Paste slip text
                    </h3>

                    <Textarea
                        placeholder="Paste your bet slip text here..."
                        value={pastedText}
                        onChange={(e) => setPastedText(e.target.value)}
                        className="min-h-[100px]"
                    />
                </div>


                <Separator className="my-6" />


                {/* ====== UPLOAD SCREENSHOT ====== */}
                <div className="space-y-3">
                    <h3 className="font-medium flex items-center gap-2">
                        <Upload className="w-4 h-4 text-primary" />
                        Upload screenshot
                    </h3>

                    <Input
                        type="file"
                        accept="image/*"
                        onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                    />

                    {file && (
                        <p className="text-sm text-muted-foreground">
                            Selected: {file.name}
                        </p>
                    )}
                </div>


                <Separator className="my-6" />


                {/* ====== CONNECT SPORTSBOOK (FUTURE) ====== */}
                <div className="space-y-3">
                    <h3 className="font-medium flex items-center gap-2">
                        <LinkIcon className="w-4 h-4 text-primary" />
                        Connect sportsbook (optional)
                    </h3>

                    <Button
                        variant="outline"
                        disabled
                        className="opacity-70 cursor-not-allowed"
                    >
                        Coming Soon…
                    </Button>

                    <p className="text-sm text-muted-foreground">
                        Read-only integration with DraftKings, FanDuel, BetMGM, and others.
                    </p>
                </div>


                {/* ====== ACTIONS ====== */}
                <DialogFooter className="mt-4">
                    <DialogClose asChild>
                        <Button variant="outline">Cancel</Button>
                    </DialogClose>

                    <Button onClick={handleImport}>Import Bets</Button>
                </DialogFooter>
            </DialogContent>
        </Dialog>
    )
};
