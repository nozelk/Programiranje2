import java.util.Scanner;

public class Collatzovo_zap {
    public static int vpis() {
        Scanner scr = new Scanner(System.in);

        System.out.print("Number: ");
        int n = scr.nextInt();

        return n;
    }

    public static void sequence(int n){
        System.out.print("Sequence:");
        do{
            System.out.print(" "+ n);
            if (n % 2 == 0){
                n /= 2;

            }
            else{
                n = 3 * n + 1;
            }
        }while (n != 1);
        System.out.print(" 1");
    }

    public static int length(int n){
        int stej = 0;
        do{
            stej += 1;
            if (n % 2 == 0){
                n /= 2;

            }
            else{
                n = 3 * n + 1;
            }
        }while (n != 1);
        return stej + 1;
    }

    public static int maximum(int n){
        int max = n;
        do{
            if (n % 2 == 0){
                n /= 2;

            }
            else{
                n = 3 * n + 1;
            }
            if (max < n){
                max = n;
            }
        }while (n != 1);
        return max;
    }
    public static void main(String[] args) {
        /*int n = vpis();
        
        System.out.println("Length: "+ length(n));
        System.out.println("Maximum: "+ maximum(n));
        sequence(n);
        */
        for (int m : new int[] { 6, 12, 19, 27, 871 }) {
            System.out.format("Number: %,d\n", m);
            System.out.format("Length: %,d\n", length(m));
            System.out.format("Maximum: %,d\n", maximum(m));

            System.out.print("Sequence: ");
            sequence(m);
            System.out.println();
        }
    }
}