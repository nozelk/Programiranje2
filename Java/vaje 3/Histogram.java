import java.io.*;
import java.util.*;

public class Histogram {
    private int velikost;
    private int sirina;
    private int maximum;
    private int[] histogram;

    public Histogram(List<Integer> stevila, int sirina, int maximum) {
        this.velikost = stevila.size();
        this.sirina = sirina;
        this.maximum = maximum;
        this.histogram = new int[(maximum + sirina - 1) / sirina];
        for (int num : stevila) {
            this.histogram[num / sirina]++;
        }
    }

    public int getVelikost() {
        return velikost;
    }

    public int getSirina() {
        return sirina;
    }

    public int getMaximum() {
        return maximum;
    }

    public int[] getHistogram() {
        return histogram;
    }

    @Override
    public String toString() {
        String niz = "";
        for (int i = 0; i < histogram.length; i++) {
            if (i > 0) niz += "\n";
            niz += String.format(
                    Locale.ENGLISH, 
                    "%10s: %3d - %4.1f%%", 
                    "[" + i * sirina + "," + Math.min(maximum, (i + 1) * sirina) + ")", 
                    histogram[i], 
                    100.0 * histogram[i] / velikost
                );
        }
        return niz;
    }

    static final int MAXIMUM = 123;

    public static void zapisi(String izhodna) throws IOException {
        Random random = new Random();
        int M = MAXIMUM;
        int lines = 1000;
        try (PrintWriter writer = new PrintWriter(new File(izhodna))) {
            for (int i = 0; i < lines; i++){
                int st = random.nextInt(5) + 1;
                for (int j = 0; j < st; j++){
                    int n = random.nextInt(M);
                    if ((j + 1) == (st)) writer.println(n);
                    else writer.print(n + " ");
                }
            }
        }
    }

    public static List<Integer> preberi(String vhodna) throws IOException {
        List<Integer> numbers = new ArrayList<>();
        try (Scanner scanner = new Scanner(new File(vhodna))) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine();
                String[] tokens = line.split("\\s+");
                for (String token : tokens) {
                    int number = Integer.parseInt(token);
                    numbers.add(number);
                }
            }
        }
        return numbers;
    }

    public static void main(String[] args) {
        List<Integer> stevila = null;
        try {
            zapisi("stevila.txt");
            stevila = preberi("stevila.txt");
        } 
        catch (IOException e) {
            e.printStackTrace();
            System.exit(0);
        }
        Histogram histogram = new Histogram(stevila, 12, MAXIMUM);
        System.out.println(histogram);
    }
}