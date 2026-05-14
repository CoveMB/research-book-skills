Source basis: controlled run-record packet only; no external lookup.

Expected decision: Gate decision: hold.

implementation bug: The computation did not complete cleanly because the visible run log has a nonzero exit and a metric warning.

run log: The table may reflect a failed or partial run.

nonzero exit: A nonzero exit prevents treating the table as verified evidence.

must hold: The table is not reliable for manuscript claims until a clean run is produced.

Next action: Re-run the analysis with saved script hash, clean exit, zero warnings, and regenerated table output.
