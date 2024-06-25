import java.util.Scanner;

public class KotMedKazalcoma {
    public static void main(String[] args) {
        Scanner scr = new Scanner(System.in);
        int ure = 0;
        int minute = 0;
        boolean flag = false;

        do {
            System.out.print("Vnesite uro: ");
            String time = scr.nextLine();
            String[] parts = time.split(":");
            ure = Integer.parseInt(parts[0]);
            minute = Integer.parseInt(parts[1]);

            if (ure >= 0 && minute >= 0 && ure <= 12 && minute < 60) {
                flag = true;
            }
        } while (!flag);

        kot(ure, minute);
    }
    public static void kot(int ure, int minute) {
        if (ure == 12) {
            ure = 0;
        }

        if (minute == 60) {
            minute = 0;
            ure += 1;
        }
        double kot_ure = 0.5 * (ure * 60 + minute);
        double kot_minute = 6 * minute;
        double alfa = Math.abs(kot_ure - kot_minute);
        alfa = Math.min(360 - alfa, alfa);
        int stopinje = (int)alfa;
        int minute_kot = (int)((alfa - stopinje) * 60);
        if (minute_kot == 0) {
            System.out.printf("Ob %02d:%02d je kot med kazalcema enak %d stopinj.\n", ure, minute, stopinje);
        } else {
            System.out.printf("Ob %02d:%02d je kot med kazalcema enak %d stopinj in %d minut.\n", ure, minute, stopinje, minute_kot);
        }
    }
}
