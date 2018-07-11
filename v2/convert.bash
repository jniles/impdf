#!/usr/bin/env bash

SITE="https://www.internationalministries.org"
SLUG="haiti-pigs-for-kids"
OUTPUT="$SLUG.pdf"

RENDERER="weasyprint"

echo "Printing: $SITE/$SLUG to $OUTPUT"
if [ "$RENDERER" = "weasyprint" ]; then
  echo "Using weasyprint"
  weasyprint --encoding utf8 --stylesheet stylesheet.css --presentational-hints "$SITE/$SLUG" $OUTPUT

# in practice, this turns out so much worse.  Six whole pages!
else
  echo "Using wkhtmltopdf"
  wkhtmltopdf --encoding utf8 --user-style-sheet stylesheet.css --page-size Letter "$SITE/$SLUG" $OUTPUT
fi

echo "Saved to $OUTPUT"
