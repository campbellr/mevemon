#
# Makefile for mEveMon (inspired by the Makefile for Heremes)
# 

compile:
	perl -ni -e 'print; exit if /^XB-Maemo-Icon-26:$$/' debian/control
	uuencode -m share/mevemon-48.png - | perl -ne 'print " $$_" unless $$. == 1 or /^====$$/' >>debian/control



install:
	mkdir -p ${DESTDIR}/opt/mevemon/ ${DESTDIR}/opt/mevemon/eveapi ${DESTDIR}/opt/mevemon/ui \
	${DESTDIR}/opt/mevemon/ui/diablo ${DESTDIR}/opt/mevemon/ui/fremantle
	install -D -m 0644 -o root -g root src/*.py ${DESTDIR}/opt/mevemon/
	install -D -m 0644 -o root -g root src/eveapi/*.py ${DESTDIR}/opt/mevemon/eveapi/
	install -m 0644 -o root -g root src/ui/*.py  ${DESTDIR}/opt/mevemon/ui/
	install -D -m 0644 -o root -g root src/ui/fremantle/*.py  ${DESTDIR}/opt/mevemon/ui/fremantle/
	install -D -m 0644 -o root -g root src/ui/diablo/*.py  ${DESTDIR}/opt/mevemon/ui/diablo/
	install -D -m 0644 -o root -g root share/mevemon-64.png \
	${DESTDIR}/usr/share/icons/hicolor/scalable/hildon/mevemon.png
	install -D -m 0644 -o root -g root share/mevemon-48.png \
	${DESTDIR}/usr/share/icons/hicolor/48x48/hildon/mevemon.png
	install -D -m 0644 -o root -g root share/mevemon.desktop \
	${DESTDIR}/usr/share/applications/hildon/mevemon.desktop
	chmod 755 ${DESTDIR}/opt/mevemon/mevemon.py

clean:
	rm -f src/*.py[oc]
	rm -f src/ui/fremantle/*.py[oc]
	rm -f src/ui/diablo/*.py[oc]
	rm -f src/eveap/*.py[oc]
	rm -f build-stamp configure-stamp
	find . -name *~ -exec rm -f {} \;	

package:
	dpkg-buildpackage -rfakeroot -uc -us
