# PDF to reference network

```
source run.sh
// cat ref.json
```

will produce reference network among scholarly papers saved in

```
pdfs
```

---------

# Reference detection
Very naive. A.pdf is referencing B.pdf if [text under REFERENCE of A] includes certain amount of words exist in [certain amount of words from the head of B].


# Visualizer
The output json is in a format for gaNeza (visualizer).
See [https://github.com/arcoyk/gaNeza](https://github.com/arcoyk/gaNeza)


