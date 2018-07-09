#!/usr/bin/env bash

SITE="https://www.internationalministries.org"
SLUG="haiti-pigs-for-kids"
OUTPUT="$SLUG.pdf"

echo "Printing: $SITE/$SLUG to $OUTPUT"

weasyprint --encoding utf8 --stylesheet stylesheet.css --presentational-hints "$SITE/$SLUG" $OUTPUT

echo "Saved to $OUTPUT"
