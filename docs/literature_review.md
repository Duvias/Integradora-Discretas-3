# Literature review

## Regular expressions

A regular expression describes a set of strings (a regular language) using
literals and operators: concatenation, union (|) and Kleene star (*)
(CyED III, slides 2). Extended notation used in practice: character classes
([a-z], \d, \w), quantifiers (?, +, {m,n}), anchors (^, $) and word
boundaries (\b).

In Python they are implemented by the re module: re.compile builds a pattern,
search finds the first match, findall/finditer find all matches and
group() returns the matched text or a captured group (CyED III, slides 2-3).

Applications: searching and replacing text, validating input (emails, phone
numbers), lexical analysis and information extraction from documents.

Use in ResumeLens: stage 1 uses regular expressions to detect strings that may
represent candidate data (email, phone, links, degrees) and qualifications.
This stage only detects candidates; it does not decide equivalences or profiles.

## Finite-state transducers

A finite-state transducer is a finite automaton that also writes output:
each transition reads an input symbol and produces a (possibly empty) string
of output symbols. It is one of the automaton types of the course, together
with DFA, NFA and ε-NFA (CyED III, slides 1).

Formal definition used in this project: M = (Q, Σ, Γ, δ, ω, q0, F), where
Q are the states, Σ the input alphabet, Γ the output alphabet, δ the
transition function, ω the output function, q0 the initial state and F the
accepting states.

Applications: translation between representations, spelling normalization,
morphological analysis and text-to-token conversion.

Use in ResumeLens: stage 2 uses transducers built with pyformlang to
translate equivalent forms of a qualification ("JS", "Javascript") into one
canonical symbol (JAVASCRIPT).