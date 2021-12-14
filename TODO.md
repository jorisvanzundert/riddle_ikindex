We kunnen nu voor elke FULLTEXT een rolling (per token) i-index draaien op 200 woorden (kan ook andere lengte, maar 200 is gebaseerd op de observatie dat 250 woorden betekenisvolle waardes voor de i-index oplevert, en dit matcht met de intuïtie dat een alinea steeds ongeveer 250 woorden lang (check of dit op cijfers in het Riddle corpus is gebaseerd)).

Wat we nu willen is het effect/bijdrage van dialoog op de waarde van de i-index zichtbaar maken. Dit doen we als volgt:

* maak grafiek i-index op full text
* maak we een gemaskeerde variant van de full text waar we alle dialoogwoorden wegfilteren door deze te matchen met de dialoog geïsoleerd door Lisanne in de folder 'dialogue only'. We vervangen dialoogwoorden door een woord dat niet door de i-index geteld word, dus 'dtoken'.

Wat we hier dan testen is de hypothese dat het effect van dialoog op de i-index in feite het perspectief 'biased' richting 1e persoons perspectief. Ook bekend uit theory (Bal), ookk Artsjom et al. beschrijven dat effect. Maar dit fenomeen is nog niet heel sterk empirisch geobserveerd/beschreven.
