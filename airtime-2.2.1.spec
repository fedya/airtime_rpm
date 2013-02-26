Name: 		airtime
Version: 	2.2.1
Release:        7%{?dist}
Summary:	Airtime is an open source application that provides remote automation of a radio station.

Group:		Development/Libraries
License:	GNU General Public License v3.0 only

URL:		http://airtime.sourcefabric.org/
Source0:	http://sourceforge.net/projects/airtime/files/2.2.1/airtime-2.2.1.tar.gz
#Source0:	%{name}-%{version}.tar.gz
Source1:        init.d-scripts.tgz

Prefix:		/

BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:          tar
BuildRequires:          gzip
BuildRequires:          curl
BuildRequires:          php-pear
BuildRequires:          postgresql
BuildRequires:          python
BuildRequires:          patch
BuildRequires:          lsof
BuildRequires:          sudo
BuildRequires:          postgresql-server
BuildRequires:          httpd
BuildRequires:          php-pgsql
BuildRequires:          php-gd
BuildRequires:          php
BuildRequires:          wget
BuildRequires:          make
BuildRequires:          redhat-lsb
BuildRequires:          python-configobj
BuildRequires:          erlang
BuildRequires:          rabbitmq-server
BuildRequires:          liquidsoap
BuildRequires:          ocaml
BuildRequires:          ocaml-findlib
BuildRequires:          libao
BuildRequires:          libao-devel
BuildRequires:          libmad
BuildRequires:          taglib
BuildRequires:          taglib-devel
BuildRequires:          libvorbis
BuildRequires:          libvorbis-devel
BuildRequires:          libtheora
BuildRequires:          libtheora-devel
BuildRequires:          pcre
BuildRequires:          ocaml-camlp4
BuildRequires:          ocaml-camlp4-devel
BuildRequires:          pcre
BuildRequires:          pcre-devel
BuildRequires:          gcc-c++
BuildRequires:          libX11
BuildRequires:          libX11-devel
BuildRequires:          flac
BuildRequires:          vorbis-tools
BuildRequires:          monit
BuildRequires:          php-bcmath
BuildRequires:          icecast
BuildRequires:          php-process
BuildRequires:          php-ZendFramework-Db-Adapter-Pdo-Pgsql
BuildRequires:          python-virtualenv

#Requires:
Requires:          tar
Requires:          gzip
Requires:          curl
Requires:          php-pear
Requires:          postgresql
Requires:          python
Requires:          patch
Requires:          lsof
Requires:          sudo
Requires:          postgresql-server
Requires:          httpd
Requires:          php-pgsql
Requires:          php-gd
Requires:          php
Requires:          wget
Requires:          make
Requires:          redhat-lsb
Requires:          python-configobj
Requires:          erlang
Requires:          rabbitmq-server
Requires:          liquidsoap
Requires:          ocaml
Requires:          ocaml-findlib
Requires:          libao
Requires:          libao-devel
Requires:          libmad
Requires:          taglib
Requires:          taglib-devel
Requires:          libvorbis
Requires:          libvorbis-devel
Requires:          libtheora
Requires:          libtheora-devel
Requires:          pcre
Requires:          ocaml-camlp4
Requires:          ocaml-camlp4-devel
Requires:          pcre
Requires:          pcre-devel
Requires:          gcc-c++
Requires:          libX11
Requires:          libX11-devel
Requires:          flac
Requires:          vorbis-tools
Requires:          monit
Requires:          php-bcmath
Requires:          icecast
Requires:          php-process
Requires:          php-ZendFramework-Db-Adapter-Pdo-Pgsql
Requires:          python-virtualenv



%description
Airtime lets you take total control of your radio station
via the web with intelligent archive management, powerful
search, a simple scheduling calendar, smart playlists,
live assist, stream rebroadcast and rock-solid automated
playout. Those who need a little extra will love the
ability to manage staff, use FLAC, WAV, AAC and
ReplayGain, upload to SoundCloud automatically, stream
multiple bandwidths to Icecast or Shoutcast and display
programme information via Airtime's website widgets.


%prep
%setup -q
tar -xvf %SOURCE1

%build
%install


echo "build \n"
mkdir -p %{buildroot}/etc/httpd/conf.d/

cp ./install_full/apache/airtime-vhost %{buildroot}/etc/httpd/conf.d/airtime.conf
sed -i 's#DocumentRoot.*$#DocumentRoot /var/www/html/airtime/public#g' %{buildroot}/etc/httpd/conf.d/airtime.conf
sed -i 's#<Directory .*$#<Directory /var/www/html/airtime/public>#g' %{buildroot}/etc/httpd/conf.d/airtime.conf
mkdir -p %{buildroot}/var/www/html/airtime
cp -R ./airtime_mvc/* %{buildroot}/var/www/html/airtime/

mkdir -p %{buildroot}/srv/airtime/stor
mkdir -p %{buildroot}/var/log/airtime
mkdir -p %{buildroot}/etc/monit/conf.d
mkdir -p %{buildroot}/etc/monit.d
mkdir -p %{buildroot}/etc/init.d/
mkdir -p  %{buildroot}/usr/lib/airtime/


echo "include /etc/monit/conf.d/*" > %{buildroot}/etc/monit.d/monit

cp -r ./python_apps %{buildroot}/usr/lib/airtime/

cp -r ./utils %{buildroot}/usr/lib/airtime/

touch  %{buildroot}/var/log/airtime/zendphp.log
cp  init.d-scripts/* %{buildroot}/etc/init.d/

%pre
for user in airtime pypo; do
        getent passwd $user >/dev/null;
        if [ 0 -eq "$?" ]; then
                echo "user $user alredy exist";
        else
                adduser --system --user-group $user;
        fi
done
%post

cp /etc/init.d/airtime-* ./

mkdir /etc/airtime

CHAR="[:alnum:]"
rand=`cat /dev/urandom | tr -cd "$CHAR" | head -c ${1:-32}`
sed -i "s/api_key = .*$/api_key = $rand/g" /etc/airtime/airtime.conf


/usr/lib/airtime/python_apps/python-virtualenv/virtualenv-install.sh

cp /var/www/html/airtime/build/airtime.conf /etc/airtime/airtime.conf


CHAR="[:alnum:]"
rand=`cat /dev/urandom | tr -cd "$CHAR" | head -c ${1:-32}`
sed -i "s/api_key = .*$/api_key = $rand/g" /etc/airtime/airtime.conf

python /usr/lib/airtime/python_apps/api_clients/install/api_client_install.py

cp -R  /usr/lib/airtime/python_apps/std_err_override /usr/lib/airtime
python /usr/lib/airtime/python_apps/media-monitor/install/media-monitor-copy-files.py
python /usr/lib/airtime/python_apps/media-monitor/install/media-monitor-initialize.py
python /usr/lib/airtime/python_apps/pypo/install/pypo-copy-files.py
cp -R /usr/lib/airtime/python_apps/api_clients/ /usr/lib/airtime
python /usr/lib/airtime/python_apps/pypo/install/pypo-initialize.py

sed -i "s/api_key = .*$/api_key = \'$rand\'/g"   /etc/airtime/api_client.cfg

rm  /etc/init.d/airtime-*
cp airtime-* /etc/init.d/
chmod +x /etc/init.d/airtime-*


echo "configure \n"
#PHP
echo "date.timezone = \"Europe/Moscow\"
upload_tmp_dir = /tmp
phar.readonly = Off" >> /etc/php.ini
echo "LANG=en_US.UTF-8" > /etc/default/locale
echo "psotgres configure"

service postgresql initdb

mv /var/lib/pgsql/data/pg_hba.conf /var/lib/pgsql/data/pg_hba.conf.save

echo "
local   all         all                               ident
host    all         all         127.0.0.1/32          md5
host    all         all         ::1/128               md5
" > /var/lib/pgsql/data/pg_hba.conf

service postgresql stop
service postgresql start

sudo -u postgres psql -c "CREATE USER airtime ENCRYPTED PASSWORD 'airtime' LOGIN CREATEDB NOCREATEUSER;"

sudo -u postgres createdb -O airtime --encoding UTF8 airtime

cd /var/www//html/airtime/build/sql/

sudo -u airtime psql --file schema.sql airtime

    sudo -u airtime psql --file sequences.sql airtime
    sudo -u airtime psql --file views.sql airtime
    sudo -u airtime psql --file triggers.sql airtime
    sudo -u airtime psql --file defaultdata.sql airtime
    sudo -u airtime psql -c "INSERT INTO cc_pref (keystr, valstr) VALUES ('system_version', '2.2.1');"
    sudo -u airtime psql -c "INSERT INTO cc_music_dirs (directory, type) VALUES ('/srv/airtime/stor', 'stor');"
    sudo -u airtime psql -c "INSERT INTO cc_pref (keystr, valstr) VALUES ('timezone', 'UTC')"
    unique_id=`php -r "echo md5(uniqid('', true));"`
    sudo -u airtime psql -c "INSERT INTO cc_pref (keystr, valstr) VALUES ('uniqueId', '$unique_id')"
    sudo -u airtime psql -c "INSERT INTO cc_pref (keystr, valstr) VALUES ('import_timestamp', '0')"


service httpd start
#chkconfig httpd on

service icecast start
#chkconfig icecast on

service rabbitmq-server start
#chkconfig rabbitmq-server on



#cp init.d/airtime-liquidsoap /etc/init.d/airtime-liquidsoap
#chmod +x /etc/init.d/airtime-liquidsoap

#cp init.d/airtime-playout  /etc/init.d/airtime-playout
#chmod +x /etc/init.d/airtime-playout

#cp init.d/airtime-media-monitor /etc/init.d/airtime-media-monitor
#chmod +x /etc/init.d/airtime-media-monitor
echo "start airtime sevices";

for i in airtime-media-monitor airtime-playout airtime-liquidsoap ; do
	chmod +x /etc/init.d/$i
	service $i stop;
	service $i start;
done


#echo "chown -R  apache: /srv/airtime/stor";
sleep 5;
chown -R apache: /srv/airtime/stor


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
/usr/lib/airtime/*
/var/www/html/airtime*
%attr(755,root,root) /etc/init.d/airtime-*
%attr(755,apache,apache) /srv/airtime*
%attr(644,apache,apache) /var/log/airtime/zendphp.log
%config
/etc/monit.d/monit*
/etc/httpd/conf.d/airtime.conf
/etc/monit/conf.d/
