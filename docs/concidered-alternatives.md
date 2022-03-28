---
nav_order: 9
---
# Considered alternatives

When designing this solution to typeset complete proceedings, several alternatives were investigated.
Nearly all possible alternatives are listed at <http://www.ctan.org/topic/confproc>.
In the following, evaluated alternatives are listed and discussed.

## confproc

[confproc](http://www.ctan.org/pkg/confproc) seems to the most suitable alternative.
Compared with this approach, it has following drawbacks:

* The PDFs of the papers do not take a proper heading (page numbers, editor).
* When clicking on a link in one included PDF, the linked PDF is opened instead of jumping to the link.
* Indexing of authors has to be done by manually.

## combine

The [combine](https://www.ctan.org/pkg/combine) class combines the sources of different LaTeX together.
Since there might be conflicting packges, we wanted to include each PDF on its own.
The PDFs can be typeset by itself.

## proc

[proc](http://www.ctan.org/pkg/proc) is a very basic class based on the article class.
No update since 1995.

## Springer Computer Science Proceedings

Springer offers help for proceedings authors at <https://www.springer.com/gp/computer-science/lncs/editor-guidelines-for-springer-proceedings>.
It uses makeindex instead of biblatex for index generation.
We opted for biblatex+texindy to be UTF-8 save and to directly be able to use the content of `\authors` for index generation.

## Further reading

* tex.stackexchange: [Constructing conference proceedings](http://tex.stackexchange.com/q/124942/9075)
