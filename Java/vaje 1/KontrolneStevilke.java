import java.util.Scanner;

public class KontrolneStevilke {
    public static String Vpisi_k_s() {
        Scanner scr = new Scanner(System.in);
        String k_s;
        do{
            System.out.print("Vpisi kontrolno številko: ");
            k_s = scr.nextLine();

        }while(k_s.length() != 12);
        

        return k_s;
    }

    public static void main(String[] args) {
        String v_s = Vpisi_k_s();
        int mnozenje = 2;
        int vsota = 0;
        for(char stevilka : v_s.toCharArray()){
            int s = Integer.parseInt(String.valueOf(stevilka));
            vsota += s * mnozenje;
            mnozenje += 1;
        }
        int ostanek;
        ostanek = vsota % 11;

        Long stevilo = Long.parseLong(v_s);
        long rez = (ostanek < 10) ? stevilo * 10 + ostanek : stevilo * 10;
        System.out.println("Število " + v_s + " ima kontrolno števko " + ostanek + ", torej je sklic enak " + rez);
    }
}