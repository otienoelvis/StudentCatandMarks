 function calculatea() {

        var c = document.getElementById('a1').value;
        var d = document.getElementById('a2').value;
        c=parseInt(c);
        d=parseInt(d);
        var e = c+d;
        document.getElementById('a3').value = e;

        var f = document.getElementById('a3').value
            switch(true){
            case (f>=70):
            document.getElementById('ag').value="A";
            break;
            case ((f>=60)&&(f<70)):
            document.getElementById('ag').value="B";
            break;
            case ((f>=50)&&(f<60)):
            document.getElementById('ag').value="C";

            break;
            case ((f>=40)&&(f<50)):
            document.getElementById('ag').value="D";
            break;
            break;
            case ((f>=0)&&(f<40)):
            document.getElementById('ag').value="F";
            break;
            case ((f==0)):
            document.getElementById('ag').value="**";
        }
    }