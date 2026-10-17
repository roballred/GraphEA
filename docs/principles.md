# Principles

The beliefs that guide GraphEA's design. For the concrete rules that
follow from them, see [design rules](design-rules.md).

1. **Curated, not automated.** Human judgment decides what is true in
   the graph. An LLM helps by proposing; it doesn't decide.
   ([0002](decisions/0002-curated-graphrag.md))
2. **Trust is visible.** Every record shows where it came from and
   whether a human has checked it, so nobody has to guess how far to
   trust it. ([0010](decisions/0010-origin-and-verification.md))
3. **Relationships are first-class.** In enterprise architecture, how
   things relate is the knowledge. Relationships deserve the same care
   as the things they connect. ([0011](decisions/0011-edges-as-records.md))
4. **LLM work is deliberate.** LLM work happens when it is directed,
   not as a side effect of running a pipeline.
   ([0012](decisions/0012-extraction-runs.md))
5. **Fix upstream.** Correct the cause, never the output. Generated
   content is fixed by changing what generates it.
6. **Start loose, tighten later.** New fields and constraints start
   optional. Tightening a schema is easier than loosening one after
   records depend on it.
7. **Assume variability; preserve options.** Sources, refresh rates and
   consumers will change. Use neutral formats, and don't commit to a
   database, vector store or consumer before it's needed.
