# MozesCachelabVisualisatie

Gebruik dit script op eigen risico! Dit script kan handig zijn als visuele ondersteuning bij het CacheLab.
Creert twee .png bestandjes met daarin heatmaps voor cachegebruik bij Store en Load operaties.

De boel is redelijk gehardcode dus verwacht bugs.

# script arguments
    dim: M N - Dimensies van de matrix waarvoor je wilt testen
    offset: N - Aantal lines van de trace file om over te slaan. Je wilt eigenlijk alle data memory accesses 
                die je doet voor je main loopjes niet mee laten nemen in het maken van de heatmap, kijk in 
                je tracefile of je kunt ontdekken vanaf wanneer je alleen nog aan de matrices zit in data 
                memory (bij de meegeleverde naive implementatie is de juiste offset 4).
    
# usage
    
Download `mozes.py` of clone de repo, en plaats het in je cachelab folder. Volgende command runt test-trans voor M=32, N=32, runt de sim op de resulterende tracefile, en creert hier een heatmap van, waarbij de eerste 4 regels van de tracefile worden genegeerd.

        ./python3 mozes.py 32 32 --offset 4 

# requirements

    python3
    matplotlib

Met dank aan Mozes vd Kar.

Known bugs: voor 61x67 klopt de output van geen kant
