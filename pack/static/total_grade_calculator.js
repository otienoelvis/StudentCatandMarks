 function calculator() {

        var c = document.getElementById('c1').value;
        var d = document.getElementById('c2').value;
        var b = document.getElementById('m1').value;
        c=parseInt(c);
        d=parseInt(d);
        b=parseInt(b);


        var e = ((c+d)/2) + b;
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