# Notes on Porting a Shell Script to a Makefile

Summarizes the insights gained while porting `batch.sh` to `Makefile`.

## Structural Mapping

| Shell script | Makefile |
|---|---|
| Top-level processing block | `.PHONY` target |
| `for` loop | Split into multiple targets |
| `[ -f file ] \|\| continue` | Prerequisite of a static pattern rule |
| Shell variable assignment `x=val` | Make variable `X = val` |

## Static Pattern Rules

Checking for a prerequisite file's existence can be delegated to Make.

```makefile
$(TOPICS): %: ../%-fr.txt ../%-en.txt
    ...
```

If the target file doesn't exist, Make reports an error. This removes the need for `continue` inside a loop.

## Lazy Evaluation of Variables Containing `$@`

A variable defined with `=` is expanded at recipe execution time, so it can include `$@` (the target name).

```makefile
FR_FILE = ../$@-fr.txt  # $@ is expanded inside the recipe
```

However, `$@` is undefined in the prerequisite list, so it can't be used there. Moving to a static pattern rule removes the need for the variable itself.

## Splitting Processing via a Target Hierarchy

```makefile
all: common core extra
core: $(TOPICS)
$(TOPICS): %: ...
```

The shell's processing order is expressed through target dependencies, and individual runs (e.g. `make onde`) also become possible.

## `define` Is Equivalent to Inline Expansion

Makefile's `define` is text substitution, not an abstraction like a function. A shared recipe is clearer written directly in a multi-target rule.

```makefile
# Writing it directly is clearer than define RECIPE ... endef + $(RECIPE)
$(TOPICS): %: ...
    <shared recipe>
```

## Caveat on Variable Names

Watch out for collisions with variable names used by Make or the shell, such as `TERM`, `SHELL`, `MAKE`.
