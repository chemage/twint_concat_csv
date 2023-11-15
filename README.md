# Twint CSV Concatenation

Concatenate Twint CSV files.

Twint provides us with mostly one file per transaction and there seems 
to be no way of exporting a single file with all transactions.

Each of these CSV exports is composed of "two" CSV files.

Example:
```
"Datum Überweisung";"27.02.2023"
"Datum Abrechnung";"26.02.2023"
"Währung";"CHF"
"Überweisung am";"Transaktionsgebühr";"Währung";"Gutgeschriebener Betrag";"Kennung Verkaufsstelle";"UUID Store";"Betrag Transaktion";"Währung";"Transaktionsdatum";"Transaktionszeit";"Typ";"Order ID";"Terminal ID";"Transaktions-ID";"Händlertransaktions-ID"
```

After the "real" header row, there is a data line (there could be several).

The script skips the first three lines and actually starts reading from the header line.
