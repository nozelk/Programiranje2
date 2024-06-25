import java.awt.Dimension;
import java.awt.Graphics;
import javax.swing.JFrame;
import javax.swing.JPanel;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.MouseMotionListener;
import java.util.ArrayList;
import java.util.List;
import java.awt.Color;
import java.awt.BorderLayout;

public class Circles extends JFrame {
    private List<Krog> krogi;
    private Krog selectedKrog = null;
    private int offsetX, offsetY;

    public Circles() {
        super();
        krogi = new ArrayList<Krog>();
        setTitle("Circles");
        setSize(new Dimension(1024, 768));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        JPanel panel = new JPanel(){
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                for (Krog krog : krogi) {
                    int x = (int) (krog.getX());
                    int y = (int) (krog.getY());
                    int polmer = krog.getPolmer();
                    Color barva = krog.getBarva();

                    g.setColor(barva);
                    g.fillOval(x - polmer, y - polmer, 2 * polmer, 2 * polmer);
                    g.setColor(Color.BLACK);
                    g.drawOval(x - polmer, y - polmer, 2 * polmer, 2 * polmer);
                }
            }
        };

        panel.addMouseListener(new MouseListener() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (selectedKrog == null) {
                    int x = e.getX();
                    int y = e.getY();
                    int polmer = 16;
                    Color barva = Color.GRAY;
                    krogi.add(new Krog(x, y, polmer, barva));
                    System.out.println("Krog: x=" + x + ", y=" + y + ", polmer=" + polmer + ", barva=" + barva);
                    panel.repaint();
                }
            }
            @Override
            public void mousePressed(MouseEvent e) {
                int x = e.getX();
                int y = e.getY();
                selectedKrog = getKrogAt(x, y);
                if (selectedKrog != null) {
                    offsetX = x - (int) selectedKrog.getX();
                    offsetY = y - (int) selectedKrog.getY();
                }
            }
            @Override
            public void mouseReleased(MouseEvent e) {
                selectedKrog = null;
            }
            @Override
            public void mouseEntered(MouseEvent e) {}
            @Override
            public void mouseExited(MouseEvent e) {}
        });

        panel.addMouseMotionListener(new MouseMotionListener() {
            @Override
            public void mouseDragged(MouseEvent e) {
                if (selectedKrog != null) {
                    int x = e.getX();
                    int y = e.getY();
                    selectedKrog.setX(x - offsetX);
                    selectedKrog.setY(y - offsetY);
                    panel.repaint();
                }
            }
            @Override
            public void mouseMoved(MouseEvent e) {}
        });

        add(panel, BorderLayout.CENTER);
    }

    private Krog getKrogAt(int x, int y) {
        for (Krog krog : krogi) {
            int krogX = (int) krog.getX();
            int krogY = (int) krog.getY();
            int polmer = krog.getPolmer();
            int dx = x - krogX;
            int dy = y - krogY;
            if (dx * dx + dy * dy <= polmer * polmer) {
                return krog;
            }
        }
        return null;
    }

    public static void main(String[] args) {
        new Circles().setVisible(true);
    }
}

class Krog {
    private double x;
    private double y;
    private int polmer;
    private Color barva;

    public Krog(double x, double y, int polmer, Color barva) {
        super();
        this.x = x;
        this.y = y;
        this.polmer = polmer;
        this.barva = barva;
    }

    public double getX() {
        return x;
    }

    public void setX(double x) {
        this.x = x;
    }

    public double getY() {
        return y;
    }

    public void setY(double y) {
        this.y = y;
    }

    public int getPolmer() {
        return polmer;
    }

    public Color getBarva() {
        return barva;
    }
}
