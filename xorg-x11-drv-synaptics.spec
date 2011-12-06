%global tarball xf86-input-synaptics
%global moduledir %(pkg-config xorg-server --variable=moduledir )
%global driverdir %{moduledir}/input

Name:           xorg-x11-drv-synaptics
Summary:        Xorg X11 Synaptics touchpad input driver
Version:        1.2.1
Release:        5%{?dist}
URL:            http://www.x.org
License:        MIT
Group:          User Interface/X Hardware Support
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:        ftp://ftp.x.org/pub/individual/driver/%{tarball}-%{version}.tar.bz2
Source1:        10-synaptics.fdi

Patch0:         synaptics-1.2.1-timer-fix.patch
# Bug 588612 - Spurious button 2 events
Patch1:         synaptics-1.2.1-clickfinger-defaults.patch
# Bug 604483  - synaptics man page issues
Patch2:         synaptics-1.2.1-man-page-fixes.patch
# Bug 604485  - synaptics allows invalid mode to be set
Patch3:         synaptics-1.2.1-force-mode.patch


ExcludeArch:    s390 s390x

BuildRequires:  libtool pkgconfig autoconf automake
BuildRequires:  xorg-x11-server-sdk >= 1.6.0-2
BuildRequires:  libX11-devel libXi-devel
BuildRequires:  xorg-x11-util-macros >= 1.3.0

Requires:       xorg-x11-server-Xorg >= 1.6.0-2
Requires:       hal

Provides:       synaptics = %{version}-%{release}
Obsoletes:      synaptics < 0.15.0


%description
This is the Synaptics touchpad driver for the X.Org X server. The following
touchpad models are supported:
* Synaptics
* appletouch (Post February 2005 and October 2005 Apple Aluminium Powerbooks)
* Elantech (EeePC)
* bcm5974 (Macbook Air (Jan 2008), Macbook Pro Penryn (Feb 2008), iPhone
  (2007), iPod Touch (2008)

Note that support for appletouch, elantech and bcm5974 requires the respective
kernel module.

A touchpad by default operates in compatibility mode by emulating a standard
mouse. However, by using a dedicated driver, more advanced features of the
touchpad become available.

Features:

    * Movement with adjustable, non-linear acceleration and speed.
    * Button events through short touching of the touchpad ("tapping").
    * Double-Button events through double short touching of the touchpad.
    * Dragging through short touching and holding down the finger on the
      touchpad.
    * Middle and right button events on the upper and lower corner of the
      touchpad.
    * Vertical scrolling (button four and five events) through moving the
      finger on the right side of the touchpad.
    * The up/down button sends button four/five events.
    * Horizontal scrolling (button six and seven events) through moving the
      finger on the lower side of the touchpad.
    * The multi-buttons send button four/five events, and six/seven events for
      horizontal scrolling.
    * Adjustable finger detection.
      Multifinger taps: two finger for middle button and three finger for
      right button events. (Needs hardware support. Not all models implement
      this feature.)
    * Run-time configuration using shared memory. This means you can change
      parameter settings without restarting the X server.

%prep
%setup -q -n %{tarball}-%{version}
%patch0 -p1 -b .timer-fix
%patch1 -p1 -b .clickfinger-defaults
%patch2 -p1 -b .man-page
%patch3 -p1 -b .relativ-emode

%build
%configure --disable-static
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# FIXME: Remove all libtool archives (*.la) from modules directory.  This
# should be fixed in upstream Makefile.am or whatever.
find $RPM_BUILD_ROOT -regex ".*\.la$" | xargs rm -f --

install -d $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/hal/fdi/policy/20thirdparty

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_datadir}/hal/fdi/policy/20thirdparty/10-synaptics.fdi
%{driverdir}/synaptics_drv.so
%{_bindir}/synclient
%{_bindir}/syndaemon
%{_mandir}/man4/synaptics.4*
%{_mandir}/man1/synclient.1*
%{_mandir}/man1/syndaemon.1*
%doc COPYING README

%package devel
Summary:        Xorg X11 synaptics input driver
Group:          Development/Libraries

%description devel
Development files for the Synaptics TouchPad for X.Org.

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/xorg-synaptics.pc
%dir %{_includedir}/xorg
%{_includedir}/xorg/synaptics-properties.h
%{_includedir}/xorg/synaptics.h


%changelog
* Thu Jun 17 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-5
- Bump release number. Tag for 1.2.1-4 already existed (see CVS Rev 1.12)

* Thu Jun 17 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-4
- synaptics-1.2.1-man-page-fixes.patch: Update man page to bring it more
  in-line with the real information (#604483)
- synaptics-1.2.1-force-mode.patch: don't allow any mode but Relative
  (#604485)

* Fri May 21 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-3
- Add missing patch command to apply the clickfinger-defaults patch
  (#594386).

* Tue May 04 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.1-2
- synaptics-1.2.1-clickfinger-defaults: disable clickfingers if middle or
  right button was detected (#588612)

* Mon Mar 15 2010 Adam Jackson <ajax@redhat.com> 1.2.1-1
- rebase to 1.2.1
- synaptics-1.2.1-timer-fix.patch: Don't clobber the timer immediately after
  creating it. (#573669)

* Wed Jan 06 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-5
- Use global instead of define as per Packaging Guidelines
- Remove spaces/tabs mixup to silence rpmlint.

* Tue Jan 05 2010 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-4
- remove references to git builds and git matching sources aux files.
- disable autoreconf, we're building from a tarball.

* Wed Dec 09 2009 Adam Jackson <ajax@redhat.com> 1.2.0-3
- synaptics-1.2.0-timer-fix.patch: Don't free the timer in DeviceClose, since
  that gets called on VT switch. (#540248)

* Fri Nov 20 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-2
- BuildRequires xorg-x11-util-macros 1.3.0

* Fri Oct 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.2.0-1
- synaptics 1.2.0

* Mon Sep 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-7.20090907
- This time with the tarball.

* Mon Sep 07 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-6.20090907
- Update to today's git master (synaptics 1.1.99.1)

* Tue Jul 28 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-5.20090728
- Update to today's git master.

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.99-4.20090717
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-3-20090717
- Update to today's git master.

* Wed Jul 15 2009 Adam Jackson <ajax@redhat.com> - 1.1.99-2.20090710.1
- ABI bump

* Fri Jul 10 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99-2-20090710
- Update to today's git master.

* Mon Jun 22 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.99.1-20090622
- Update to today's git master.

* Tue Apr 14 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-2
- synaptics-1.1.0-synclient-64.patch: fix 64-bit integer issues with
  synclient (#494766) 

* Mon Mar 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.1.0-1
- synaptics 1.1

* Thu Mar 05 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.4-1
- synaptics 1.1, snapshot 4 (fix for 64 bit crashes)

* Wed Mar 04 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.3-1
- synaptics 1.1, snapshot 3

* Fri Feb 27 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.99.2-1
- Synaptics 1.1, snapshot 2
- Up Requires to 1.6.0-2 for XATOM_FLOAT defines.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-4
- Fix 10-synaptics.fdi, the warning added in the last commit was not
  well-formed xml.

* Mon Feb 09 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-3
- Revert last commit, this is against Fedora policy.
  https://fedoraproject.org/wiki/Packaging:Guidelines#Configuration_files

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-2
- mark the fdi file as %config(noreplace)

* Mon Feb 02 2009 Peter Hutterer <peter.hutterer@redhat.com> 1.0.0-1
- synaptics 1.0

* Mon Jan 05 2009 Peter Hutterer <peter.hutterer@redhat.com> 0.99.3-3
- Require xorg-x11-server-sdk 1.6 to build
- Update fdi file with comments on how to merge your own keys.

* Mon Dec 22 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.3-2
- Rebuild for server 1.6

* Mon Dec 15 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.3-1
- synaptics 1.0 RC 3

* Thu Dec 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.2-1
- synaptics 1.0 RC 2

* Thu Dec 4 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.1-2
- 10-synaptics.fdi: if something has capabilities input.touchpad match it.
  Don't bother about product names.

* Mon Nov 24 2008 Peter Hutterer <peter.hutterer@redhat.com>
- Fix up summary and description, provide list of supported models.

* Fri Nov 14 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.99.1-1
- synaptics 1.0 RC 1

* Tue Oct 14 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.99-0.2
- add the make-git-snapshot script.

* Tue Oct 14 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.99-0.1
- Today's git snapshot.
- Add devel subpackage.
- remove xf86-input-synaptics-0.15.2-maxtapmove.patch: driver autoscales now.

* Wed Sep 17 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.2-1
- update to 0.15.2
- remove patches merged upstream.
- xf86-input-synaptics-0.15.2-maxtapmove.patch: scale MaxTapMove parameter
  depending on touchpad height #462211

* Tue Sep 9 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.1-1
- update to 0.15.1
- remove xf86-input-synaptics-0.15.0-tap.patch: merged in upstream.
- update patches to apply against 0.15.1.
- xf86-input-synaptics-0.15.1-dont-crash-without-Device.patch: don't crash if
  neither Device nor Path is given.

* Mon Sep 8 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-6
- xf86-input-synaptics-0.15.0-edges.patch: updated to improve edge calculation
  and acceleration factors.
- xf86-input-synaptics-0.15.0-preprobe patch: pre-probe eventcomm devices for
  axis ranges if specifed with Device option.
- update fdi file to support "bcm5974" devices.

* Sun Sep 7 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-5
- update fdi file to support "appletouch" devices.

* Tue Sep 2 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-4
- xf86-input-synaptics-0.15.0-dont-lose-buttonup.patch: force a click if
  middle button emulation times out during ReadInput cycle. RH #233717.

* Thu Aug 28 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-3
- xf86-input-synaptics-0.15.0-edges.patch: reserve 5% on each side for edge
  detection.

* Mon Aug 25 2008 Adel Gadllah <adel.gadllah@gmail.com> 0.15.0-2
- Enable tapping RH #439386

* Fri Aug 7 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.15.0-1
- Initial RPM release - this is the relicensed version of the old synaptics
  package.
- Includes Changelog from synaptics package.

* Wed Aug 6 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.14.6-10
- Update Release, really this time.

* Wed Aug 6 2008 Peter Hutterer <peter.hutterer@redhat.com> 0.14.6-10
- Fix license tag and BuildRoot, reduce description line width.
 
* Tue Jun 17 2008 Adam Jackson <ajax@redhat.com> 0.14.6-9
- Fix %%fedora version comparison to be numeric not string.

* Thu Apr 10 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.14.6-8
- Build with $RPM_OPT_FLAGS, fix debuginfo (#249979).

* Fri Mar 28 2008 Rex Dieter <rdieter@fedoraproject.org> 0.14.6-7
- Synaptics default acceleration values are way slow for alps (#437039)

* Wed Mar 26 2008 Adam Jackson <ajax@redhat.com> 0.14.6-6
- synaptics-0.14.6-alps.patch: Fix the defaults on ALPS touchpads.  Values
  stolen from rhpxl.

* Tue Mar 18 2008 Matt Domsch <Matt_Domsch@dell.com> 0.14.6-5
- synaptics-0.14.6-poll-delay.patch: make poll interval user configurable
  http://www.bughost.org/pipermail/power/2008-January/001234.html
- synaptics-0.14.6-poll-200ms.patch: reduce default poll from 20ms to 200ms

* Sun Mar 09 2008 Adam Jackson <ajax@redhat.com> 0.14.6-4
- 10-synaptics.fdi: Get hal to report the X driver as synaptics for
  touchpads we support.
- synaptics-0.14.6-tap-to-click.patch: Disable tap to click by default in
  the name of accessibility.

* Wed Mar 05 2008 Dave Airlie <airlied@redhat.com> 0.14.6-3
- rebuild for ppc64

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.14.6-2
- Autorebuild for GCC 4.3

* Mon Jan 07 2008 Jarod Wilson <jwilson@redhat.com> 0.14.6-1
- Update to 0.14.6 w/permission from krh
- Adds two-finger scrolling capability on supported hardware

* Fri Nov 30 2007 Caolan McNamara <caolanm@redhat.com> 0.14.4-12
- Resolves: rhbz#396891 patch it to at least work

* Mon Oct 15 2007 Adam Jackson <ajax@redhat.com> 0.14.4-11
- Back to ExclusiveArch, buildsystem is a disaster.

* Wed Oct 03 2007 Adam Jackson <ajax@redhat.com> 0.14.4-10
- ExclusiveArch -> ExcludeArch.

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 0.14.4-9
- Rebuild for build id

* Wed Aug 16 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-8
- bump for missing ppc package
- remove 0 epoch
- add dist tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-7.1
- rebuild

* Tue May 16 2006 Kristian Høgsberg <krh@redhat.com> - 0:0.14.4-7
- Add missing build requires for libXext.

* Tue Apr 11 2006 Kristian Høgsberg <krh@redhat.com> 0:0.14.4-6
- Build as a shared object.

* Mon Apr 10 2006 Adam Jackson <ajackson@redhat.com 0:0.14.4-5
- Delibcwrap and rebuild for 7.1RC1 ABI.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-4.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0:0.14.4-4.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Jeremy Katz <katzj@redhat.com> - 0:0.14.4-4
- fix install destination too

* Fri Nov 18 2005 Jeremy Katz <katzj@redhat.com> - 0:0.14.4-3
- patch for modular X include paths

* Fri Nov 18 2005 Kristian Høgsberg <krh@redhat.com> - 0:0.14.4-2
- Remove last bits of monolithic X paths.

* Mon Nov 07 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.4-1
- Modular X.org
- New upstream version 

* Thu Aug 04 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.3-3
- Enable ppc builds as we have appletouch driver now

* Tue Jul 26 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.3-2
- Fix man page location (#164295)

* Fri Jul 22 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.3-1
- Update to 0.14.3

* Tue May 17 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.2-1
- Update to 0.14.2

* Mon May 16 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.1-1
- Update to 0.14.1

* Tue Mar 15 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.0-2
- Rebuild

* Thu Jan 06 2005 Paul Nasrat <pnasrat@redhat.com> - 0:0.14.0-1
- Update to 0.14.0
- Drop patch for 64bit as upstream now

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-5
- rebuild

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-4
- more ARCH fixes

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-3
- need to explicitely pass ARCH

* Wed Sep 01 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-2
- Add x86_64

* Mon Aug 09 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.5-1
- New version 
- Override mandir/bindir rather than patching

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.4-3
- Fix typo
- Only i386 for the moment

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.4-2
- Add ExclusiveArch

* Wed Jul 28 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.4-1
- New version

* Fri Jul 09 2004 Paul Nasrat <pnasrat@redhat.com> - 0:0.13.3-1
- New version
- Update makefile patch

* Thu Apr 01 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.5-0.fdr.1
- New version 
- Remove Imakefile

* Wed Feb 18 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.4-0.fdr.1
- New version

* Thu Feb 05 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.3-0.fdr.2
- Imakefile now builds synclient and syndaemon
- TODO manpages

* Mon Jan 19 2004 Paul Nasrat <pauln@truemesh.com> - 0:0.12.3-0.fdr.1
- Revert to imakefile and XFree86-sdk
- Include missing sdk headers - push upstream
- don't build synclient and syndaemon for now

* Sat Nov 29 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.12.1-0.fdr.1
- update to latest version
- Remove imake and XFree86-sdk magic

* Fri Oct 03 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.7-0.fdr.1
- new version

* Tue Sep 16 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.3-0.fdr.3.p11
- Build against latest XFree86-sdk

* Mon Sep 08 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.3-0.fdr.2.p11
- Use XFree86 sdk

* Sun Aug 10 2003 Paul Nasrat <pauln@truemesh.com> - 0:0.11.3-0.fdr.1.p11
- Initial RPM release.
