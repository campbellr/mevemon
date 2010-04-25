#
# Makefile for mEveMon (inspired by the Makefile for Heremes)
# 

#edit these when creating a new release
MAJOR_VER='0'
MINOR_VER='1'
PKG_VER='1'

compile:
	perl -ni -e 'print; exit if /^XB-Maemo-Icon-26:$$/' debian/control
	uuencode -m share/mevemon-48.png - | perl -ne 'print " $$_" unless $$. == 1 or /^====$$/' >>debian/control



install_fremantle:
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

install_diablo:
	mkdir -p ${DESTDIR}/usr/share/mevemon/ ${DESTDIR}/usr/share/mevemon/eveapi ${DESTDIR}/usr/share/mevemon/ui \
	${DESTDIR}/usr/share/mevemon/ui/diablo ${DESTDIR}/usr/share/mevemon/ui/fremantle
	install -D -m 0644 -o root -g root src/*.py ${DESTDIR}/usr/share/mevemon/
	install -D -m 0644 -o root -g root src/eveapi/*.py ${DESTDIR}/usr/share/mevemon/eveapi/
	install -m 0644 -o root -g root src/ui/*.py  ${DESTDIR}/usr/share/mevemon/ui/
	install -D -m 0644 -o root -g root src/ui/fremantle/*.py  ${DESTDIR}/usr/share/mevemon/ui/fremantle/
	install -D -m 0644 -o root -g root src/ui/diablo/*.py  ${DESTDIR}/usr/share/mevemon/ui/diablo/
	install -D -m 0644 -o root -g root share/mevemon-64.png \
	${DESTDIR}/usr/share/icons/hicolor/scalable/hildon/mevemon.png
	install -D -m 0644 -o root -g root share/mevemon-48.png \
	${DESTDIR}/usr/share/icons/hicolor/48x48/hildon/mevemon.png
	install -D -m 0644 -o root -g root share/mevemon-diablo.desktop \
	${DESTDIR}/usr/share/applications/hildon/mevemon.desktop
	chmod 755 ${DESTDIR}/usr/share/mevemon/mevemon.py

clean:
	rm -f src/*.py[oc]
	rm -f src/ui/fremantle/*.py[oc]
	rm -f src/ui/diablo/*.py[oc]
	rm -f src/eveap/*.py[oc]
	rm -f build-stamp configure-stamp
	find . -name *~ -exec rm -f {} \;	

package_fremantle:
	# modify debian/changelog to show current version, and then
	# modify debian/rules build option to call 'make install_fremantle'
	# There's got to be a  better way...
	# 
	sed -i 's:mevemon (.*):mevemon (${MAJOR_VER}.${MINOR_VER}-fremantle${PKG_VER}):g' debian/changelog	
	sed -i 's:$${MAKE} DESTDIR=$${CURDIR}/debian/mevemon.*:$${MAKE} DESTDIR=$${CURDIR}/debian/mevemon install_fremantle:g' debian/rules
	dpkg-buildpackage -rfakeroot -uc -us

package_diablo:
	# modify debian/changelog to show current version, and then
	# modify debian/rules build option to call 'make install_fremantle'
	# There's got to be a  better way...
	#
	sed -i 's:mevemon (.*):mevemon (${MAJOR_VER}.${MINOR_VER}-diablo${PKG_VER}):g' debian/changelog	
	sed -i 's:$${MAKE} DESTDIR=$${CURDIR}/debian/mevemon.*:$${MAKE} DESTDIR=$${CURDIR}/debian/mevemon install_diablo:g' debian/rules
	dpkg-buildpackage -rfakeroot -uc -us
