#
# Makefile for mEveMon (inspired by the Makefile for Heremes)
# 

#edit these when creating a new release
MAJOR_VER='0'
MINOR_VER='1'
PKG_VER='9'

compile:
	perl -ni -e 'print; exit if /^XB-Maemo-Icon-26:$$/' debian/control
	uuencode -m share/mevemon-48.png - | perl -ne 'print " $$_" unless $$. == 1 or /^====$$/' >>debian/control
	# this causes the build to fail in diablo auto-builder, so comment it out for now
	#py_compilefiles src/* src/eveapi/* src/ui/* src/ui/*/*


install:
	# the paths can be the same for both diablo and fremantle, since the Extras
	# auto-builder will 'optify' the fremantle package for us
	# 
	mkdir -p ${DESTDIR}/usr/share/mevemon/ ${DESTDIR}/usr/share/mevemon/eveapi \
	${DESTDIR}/usr/share/mevemon/ui ${DESTDIR}/usr/share/mevemon/ui/diablo \
	${DESTDIR}/usr/share/mevemon/ui/fremantle ${DESTDIR}/usr/bin ${DESTDIR}/usr/share/mevemon/imgs/
	install -D -m 0644 -o root -g root src/*.py ${DESTDIR}/usr/share/mevemon/
	ln -s /usr/share/mevemon/mevemon.py ${DESTDIR}/usr/bin/mevemon
	install -D -m 0644 -o root -g root src/eveapi/*.py ${DESTDIR}/usr/share/mevemon/eveapi/
	install -m 0644 -o root -g root src/imgs/*.jpg ${DESTDIR}/usr/share/mevemon/imgs/
	install -m 0644 -o root -g root src/ui/*.py  ${DESTDIR}/usr/share/mevemon/ui/
	install -D -m 0644 -o root -g root src/ui/fremantle/*.py  ${DESTDIR}/usr/share/mevemon/ui/fremantle/
	install -D -m 0644 -o root -g root src/ui/diablo/*.py  ${DESTDIR}/usr/share/mevemon/ui/diablo/
	install -D -m 0644 -o root -g root share/mevemon-64.png \
	${DESTDIR}/usr/share/icons/hicolor/scalable/hildon/mevemon.png
	install -D -m 0644 -o root -g root share/mevemon-48.png \
	${DESTDIR}/usr/share/icons/hicolor/48x48/hildon/mevemon.png
	install -D -m 0644 -o root -g root share/mevemon.desktop \
	${DESTDIR}/usr/share/applications/hildon/mevemon.desktop
	chmod 755 ${DESTDIR}/usr/share/mevemon/mevemon.py
	chmod 755 ${DESTDIR}/usr/bin/mevemon

clean:
	rm -f src/*.py[oc]
	rm -f src/ui/fremantle/*.py[oc]
	rm -rf src/ui/*.py[oc]
	rm -f src/ui/diablo/*.py[oc]
	rm -f src/eveap/*.py[oc]
	rm -f build-stamp configure-stamp
	rm -rf debian/mevemon
	find . -name *~ -exec rm -f {} \;	

package:
	# modify debian/changelog to show current version, and then
	# NOTE: if you want to use the deb in fremantle, then run maemo-optify-deb on the package
	# 		first.
	# 		This is done automatically by the Extras auto-builder 
	sed -i 's:mevemon (.*):mevemon (${MAJOR_VER}.${MINOR_VER}-${PKG_VER}):g' debian/changelog	
	dpkg-buildpackage -rfakeroot -uc -us

