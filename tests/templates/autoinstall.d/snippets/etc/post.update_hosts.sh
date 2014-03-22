destdir=$1
f=${destdir}/etc/hosts
test -f $f.save || cp $f $f.save
echo "# Added:" >> $f
echo "192.168.100.1 foo.example.com foo" >> $f
echo "192.168.100.100 bar.example.com bar" >> $f
echo "192.168.100.101 baz.example.com " >> $f
echo "192.168.100.102  hoge" >> $f
