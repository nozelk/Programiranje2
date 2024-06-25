import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class StetjeBesed {

    public static Map<String, Integer> prestej(String vhodna) throws IOException {
        Map<String, Integer> frekvence = new HashMap<>();
        try (Scanner scanner = new Scanner(new InputStreamReader(new FileInputStream(vhodna), StandardCharsets.UTF_8))) {
            while (scanner.hasNextLine()) {
                String line = scanner.nextLine().strip().toLowerCase();
                for (String beseda : line.split("\\P{L}+")) {
                    if (!beseda.isEmpty()) {
                        frekvence.put(beseda, frekvence.getOrDefault(beseda, 0) + 1);
                    }
                }
                
            }
        }
        return frekvence;
    }
    

    
    public static void izpisi(Map<String, Integer> slovar, int n) {
        List<Par> pairs = new ArrayList<>();
        for (Map.Entry<String, Integer> entry : slovar.entrySet()) {
            pairs.add(new Par(entry.getKey(), entry.getValue()));
        }

        Collections.sort(pairs);

        for (int i = 0; i < n && i < pairs.size(); i++) {
            System.out.println(pairs.get(i));
        }
    }


    public static void main(String[] args) {
        try {
            Map<String, Integer> slovar = prestej("na_klancu.txt");
            izpisi(slovar, 100);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


class Par implements Comparable<Par> {
    String word;
    Integer count;

    Par(String word, Integer count) {
        this.word = word;
        this.count = count;
    }

    @Override
    public int compareTo(Par other) {
        return other.count.compareTo(this.count);
    }

    @Override
    public String toString() {
        return word + ": " + count;
    }
}