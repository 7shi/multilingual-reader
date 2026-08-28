# Future Action Plan

Building on the success of Experiment 07 (revision via third-party evaluation), we will proceed with the following plan to optimize the revision process and expand its scope of application.

## Experiment 08: Verifying single-step revision using CoT

In Experiment 07, we adopted a two-step approach in which the evaluation model freely analyzes issues (Prompt 1) and then outputs a corrected translation based on that analysis (Prompt 2), with CoT itself disabled (`--no-think`).
We will compare this against **an approach that enables CoT (the `<think>` tag) and performs "analysis and output of the corrected translation in a single prompt" (single-step approach)**.

In this approach, the thought process (analysis) is not retained as normal text in the chat history context, but remains only within the hidden `<think>` block — a key difference.
Experiment 08 investigates how much this affects revision quality and contextual consistency, and which approach is more practical in terms of processing time.

## Expanding scope to medium-resource languages

In Experiment 08, we will compare the "two-step approach (pseudo-CoT)" and the "single-step approach (native CoT)" to determine the superior revision process (with a good balance of quality and speed).

Once the process is finalized, we plan to expand the number of target languages beyond Dutch and Czech to **other medium-resource languages that have been stuck in the 70-85 point range (Catalan, Bulgarian, Norwegian, etc.)**, to broadly verify the generality and stability of this approach.
