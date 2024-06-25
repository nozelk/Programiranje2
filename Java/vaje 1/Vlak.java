import java.util.Scanner;

public class Vlak {
    public static void main(String[] args) {
        Scanner scr = new Scanner(System.in);
        String odhod;
        String prihod;
    
        System.out.print("Odhod: ");
        odhod = scr.next();
        System.out.print("Prihod: ");
        prihod = scr.next();
        
        String[] odhods = odhod.split(":");
        String[] prihods = prihod.split(":");

        int odhod_ura = Integer.parseInt(odhods[0]);
        int odhod_minuta = Integer.parseInt(odhods[1]); 
        int prihod_ura = Integer.parseInt(prihods[0]);
        int prihod_minuta = Integer.parseInt(prihods[1]); 

        int minuta;
        int ura;

        if (prihod_minuta < odhod_minuta){
            minuta = prihod_minuta + 60 - odhod_minuta;
            ura = prihod_ura - 1 - odhod_ura;
        }
        else{
            minuta = prihod_minuta - odhod_minuta;
            ura = prihod_ura - odhod_ura;
        }

        String rezultat = String.format("%s:%s", ura, minuta);
        System.out.println("Trajanje: " + rezultat);
    }
}
