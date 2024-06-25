import java.util.Collection;
import java.util.Set;
import java.util.TreeSet;

public class Vector implements Comparable<Object>{
    TreeSet<Object> vektor = new TreeSet<Object>();

    public Vector() {
        for (int i = 0; i < 3; i++)
            vektor.add(0);
    }

    public Vector(int n) {
        for (int i = 0; i < n; i++)
            vektor.add(Math.random());
    }

    public Vector(double[] coordinates) {
        for (int i = 0; i < coordinates.length; i++)
            vektor.add(coordinates[i]);
    }

    public static void main(String[] args) {
        // Urejena množica vektorjev
        Set<Vector> set = new TreeSet<Vector>();
        set.add(new Vector());
        set.add(new Vector(3));
        set.add(new Vector(new double[] {0.0, 0.0, 0.0}));
        set.add(new Vector(new double[] {1.0, 1.0, 1.0}));
        // Izpis množice vektorjev
        for (Vector vector: set)
          System.out.println(vector);
}
    @Override
    public int compareTo(Collection<?> o) {
        this.vektor.retainAll(o);
        return 0;
    }

    
}