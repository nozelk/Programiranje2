import java.util.Scanner;

public class Pretvorba {
    public static String vpis() {
        Scanner scr = new Scanner(System.in);

        System.out.print("Vpisi yarde: ");
        String vpis = scr.nextLine();

        return vpis;
    }

    public static void main(String[] args) {
        String vpis_in = vpis();

        String[] vpis_in_ = vpis_in.split(" ");


        while(!vpis_in_[1].equalsIgnoreCase("yardov")){
            System.out.println("Naroben vnos");
            vpis_in = vpis();
            vpis_in_ = vpis_in.split(" ");
            System.out.println(vpis_in_[1]);
        }

        String stevilo = vpis_in_[0];

        float floatValue = Float.parseFloat(stevilo);
        floatValue *=  0.9144;
        String s = String.valueOf(floatValue);

        String[] vrednost = s.split("\\.");

        System.out.printf("%s m %c dm %c cm%n", vrednost[0], vrednost[1].charAt(0), vrednost[1].charAt(1));

    }
}
