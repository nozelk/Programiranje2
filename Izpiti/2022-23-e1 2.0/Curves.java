import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.ArrayList;
import java.util.List;

public class Curves extends JFrame {
    private List<Curve> curves;

    private Color getRandomColor() {
        Color[] colors = {Color.CYAN, Color.YELLOW, Color.MAGENTA};
        int barva = (int) (Math.random() * colors.length);
        return colors[barva];
    }

    public Curves() {
        super();
        setTitle("Curves");
        setLayout(new BorderLayout());
        setSize(new Dimension(1024, 768));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        curves = new ArrayList<>();

        JPanel panel = new JPanel() {
            @Override
            public void paint(Graphics g) {
                super.paint(g);
                for (Curve curve : curves) {
                    g.setColor(curve.color);
                    List<Point> tocke = curve.points;
                    if (!tocke.isEmpty()) {
                        Point prejsna_tocka = tocke.get(0);
                        for (int i = 1; i < tocke.size(); i++) {
                            Point trenutna_tocka = tocke.get(i);
                            g.drawLine(prejsna_tocka.x, prejsna_tocka.y, trenutna_tocka.x, trenutna_tocka.y);
                            prejsna_tocka = trenutna_tocka;
                        }
                    }
                }
            }
        };
        panel.setBackground(Color.WHITE);
        panel.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                super.mousePressed(e);
                Curve krivulja = new Curve(e.getX(), e.getY(), getRandomColor());
                curves.add(krivulja);
                panel.repaint();
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                super.mouseReleased(e);
                panel.repaint();
            }
        });
        panel.addMouseMotionListener(new MouseMotionAdapter() {
            public void mouseDragged(MouseEvent e) {
                super.mouseDragged(e);
                Curve trenutnaKrivulja = curves.get(curves.size() - 1);
                trenutnaKrivulja.points.add(new Point(e.getX(), e.getY()));
                panel.repaint();
            }
        });
        add(panel, BorderLayout.CENTER);

        JPanel console = new JPanel();
        console.setBackground(Color.WHITE);
        add(console, BorderLayout.NORTH);
        JButton deleteButton = new JButton("Delete");
        deleteButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                curves.clear();
                panel.repaint();
            }
        });
        console.add(deleteButton);
        
    }

    

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new Curves().setVisible(true);
            }
        });
    }
}

class Curve {
    public List<Point> points;
    public Color color;

    public Curve(int x, int y, Color color) {
        points = new ArrayList<>();
        points.add(new Point(x, y));
        this.color = color;
    }
}
