import java.util.Arrays;
import java.util.Random;
import java.util.TreeSet;

public class Vector implements Comparable<Vector> {
    private double[] coordinates;

    
    public Vector() {
        this(new double[]{0.0, 0.0, 0.0});
    }

    public Vector(int n) {
        this.coordinates = new double[n];
        Random random = new Random();
        for (int i = 0; i < n; i++) {
            this.coordinates[i] = random.nextDouble();
        }
    }

    public Vector(double[] coordinates) {
        this.coordinates = coordinates;
    }

    @Override
    public String toString() {
        return Arrays.toString(coordinates);
    }

    @Override
    public int compareTo(Vector other) {
        int dim1 = this.coordinates.length;
        int dim2 = other.coordinates.length;
        int minDim = Math.min(dim1, dim2);

        for (int i = 0; i < minDim; i++) {
            if (this.coordinates[i] != other.coordinates[i]) {
                return Double.compare(this.coordinates[i], other.coordinates[i]);
            }
        }

        return Integer.compare(dim1, dim2);
    }

    public static void main(String[] args) {
        TreeSet<Vector> set = new TreeSet<>();
        set.add(new Vector());
        set.add(new Vector(3));
        set.add(new Vector(new double[]{0.0, 0.0, 0.0}));
        set.add(new Vector(new double[]{1.0, 1.0, 1.0}));

        // Izpis množice vektorjev
        for (Vector vector : set) {
            System.out.println(vector);
        }
    }
}
