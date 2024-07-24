# Python-Course-ifgi

# 🔥🔥 Firescope 🔥🔥
Erfassen und verwalten von Bränden in Münster.
Alle Daten liegen im Ordner "Final Project"

## Starthinweise
1. Ordner "Firescope" in den Plugin Ordner von QGIS speichern:
`C:\Users\benutzer\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\`
2. Öffnen des QGIS Projektes "Firescope" aus dem Ordner "Shapefiles"
3. Aktivieren des Plugins

## Anwendung
### Branderfassung
- Durch Klicken auf "Feuer" können neue Brände erfasst werden.
- Beim Speichern wird automatisch die nächste Feuerstation bestimmt, die noch genug Fahrzeuge zur Verfügung hat.
- Die Route zur Station wird ermittelt und angezeigt.

### Brandverwaltung
- Nach Auswahl eines Brandes kann dieser auf gelöscht gesetzt werden. Dadurch wird auch die zugehörige Route gelöscht und die benutzen Fahrzeuge werden wieder der Station zugewiesen.
- Es kann außerdem ein pdf ausgespielt werden, mit Infos zu dem Brand.

### Fahrzeugverwaltung
- Es können Fahrzeuge den Stationen zugewiesen oder gelöscht werden.
- Durch klicken auf die Knöpfe werden jeweils ein Fahrzeug hinzugefügt oder gelöscht.

### Die Symbolisierung
- Ist der Status eines Brandes "gelöscht" erscheint das Feuer ausgegraut
- Sind bei einer Station alle Fahrzeuge im Einsatz wird diese auch ausgegraut
