# The prototype

`trade_defence_desk_prototype.html` is a single page. Download it and open it in a
browser. It needs no server. It loads its fonts from Google Fonts, so it looks best online.

## What it is

A clickable design study made before the capstone. It shows the screens the real desk
will have: the inbox, the case page with its six questions, the decisions list and the
proof. It also plays a pipeline run step by step.

## What it is not

- It is **not connected to anything.** All data in it is example data written into the page.
- It tells its story with a **different invented importer** (a company that buys wire
  shelving and other metal goods), not with Bergmann Outdoor. The docs in this repository use Bergmann. The
  screens and the ideas are the same.
- Its numbers are examples. None of them is a result.
- It was written before our wording rules. Where it says "residual" on its own, the real
  desk says "all other imports".

## Why it is in the repository

- Lane C starts the real screens from this file (issue C-01, decision D-11).
- Its euro engine is the JavaScript that lane C ports to Python, with 13 checks that become
  tests (issue C-03).
- For everyone else it is the fastest way to see where the project is heading.

## A good way to look at it

1. Open the inbox and pick a case.
2. Find the six questions on the case page. They are listed in
   [docs/01_PRODUCT.md](../docs/01_PRODUCT.md).
3. Answer one open decision and watch the euro range.
4. Click a number and look for the sentence behind it.
