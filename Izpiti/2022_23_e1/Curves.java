import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.util.*;

public class Curves extends JFrame {
    private ArrayList<Curve> curves; // List to store all curves

    public Curves() {
        super("Curves");
        setSize(new Dimension(1024, 768));
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        curves = new ArrayList<>();

        JPanel panel = new JPanel() {
            private Point startPoint; // Starting point for drawing curve

            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                for (Curve curve : curves) {
                    g.setColor(curve.color);
                    ArrayList<Point> points = curve.points;
                    if (points.size() > 1) {
                        Point p1 = points.get(0);
                        for (int i = 1; i < points.size(); i++) {
                            Point p2 = points.get(i);
                            g.drawLine(p1.x, p1.y, p2.x, p2.y);
                            p1 = p2;
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
                if (e.getButton() == MouseEvent.BUTTON1) { // Left mouse button
                    Color randomColor = getRandomColor();
                    curves.add(new Curve(e.getX(), e.getY(), randomColor));
                    panel.repaint();
                }
            }
        });
        panel.addMouseMotionListener(new MouseMotionAdapter() {
            @Override
            public void mouseDragged(MouseEvent e) {
                super.mouseDragged(e);
                if (SwingUtilities.isLeftMouseButton(e)) {
                    curves.get(curves.size() - 1).points.add(new Point(e.getX(), e.getY()));
                    panel.repaint();
                }
            }
        });
        add(panel, BorderLayout.CENTER);

        JPanel console = new JPanel();
        console.setBackground(Color.WHITE);
        JButton deleteButton = new JButton("Delete");
        deleteButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                curves.clear();
                panel.repaint();
            }
        });
        console.add(deleteButton);
        add(console, BorderLayout.NORTH);
    }

    private Color getRandomColor() {
        Random random = new Random();
        Color[] colors = {Color.CYAN, Color.YELLOW, Color.MAGENTA};
        return colors[random.nextInt(colors.length)];
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            new Curves().setVisible(true);
        });
    }
}

class Curve {
    public ArrayList<Point> points;
    public Color color;

    public Curve(int x, int y, Color color) {
        points = new ArrayList<>();
        points.add(new Point(x, y));
        this.color = color;
    }
}
