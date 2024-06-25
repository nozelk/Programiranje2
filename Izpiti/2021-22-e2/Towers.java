import javax.swing.*;
import java.awt.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class Towers {
    private static final int PANEL_WIDTH = 800;
    private static final int PANEL_HEIGHT = 600;
    private static final int BASE_STATIONS_COUNT = 10;
    private static final int MOBILE_DEVICES_COUNT = 10000;

    private static List<Point> baseStations;
    private static List<Point> mobileDevices;

    public static void main(String[] args) throws Exception {
        JFrame frame = new JFrame("Towers");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(new Dimension(PANEL_WIDTH, PANEL_HEIGHT));
        frame.setResizable(false);

        JPanel panel = new JPanel() {
            @Override
            public void paint(Graphics g) {
                super.paint(g);
                Graphics2D graphics = (Graphics2D) g;
                drawConnections(graphics);
            }
        };
        panel.setBackground(Color.WHITE);
        frame.add(panel);
        frame.setVisible(true);

        initializeBaseStations();
        initializeMobileDevices();

        while (true) {
            updateMobileDevices();
            panel.repaint();
            Thread.sleep(1000);
        }
    }

    private static void initializeBaseStations() {
        baseStations = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < BASE_STATIONS_COUNT; i++) {
            int x = random.nextInt(PANEL_WIDTH);
            int y = random.nextInt(PANEL_HEIGHT);
            baseStations.add(new Point(x, y));
        }
    }

    private static void initializeMobileDevices() {
        mobileDevices = new ArrayList<>();
        Random random = new Random();

        for (int i = 0; i < MOBILE_DEVICES_COUNT; i++) {
            int x = random.nextInt(PANEL_WIDTH);
            int y = random.nextInt(PANEL_HEIGHT);
            mobileDevices.add(new Point(x, y));
        }
    }

    private static void updateMobileDevices() {
        mobileDevices.clear();
        Random random = new Random();

        for (int i = 0; i < MOBILE_DEVICES_COUNT; i++) {
            int x = random.nextInt(PANEL_WIDTH);
            int y = random.nextInt(PANEL_HEIGHT);
            mobileDevices.add(new Point(x, y));
        }
    }

    private static void drawConnections(Graphics2D graphics) {
        graphics.setColor(Color.BLACK);

        for (Point mobileDevice : mobileDevices) {
            Point closestBaseStation = findClosestBaseStation(mobileDevice);
            graphics.drawLine(mobileDevice.x, mobileDevice.y, closestBaseStation.x, closestBaseStation.y);
        }
    }

    private static Point findClosestBaseStation(Point mobileDevice) {
        Point closestBaseStation = null;
        double minDistance = Double.MAX_VALUE;

        for (Point baseStation : baseStations) {
            double distance = calculateDistance(mobileDevice, baseStation);
            if (distance < minDistance) {
                minDistance = distance;
                closestBaseStation = baseStation;
            }
        }

        return closestBaseStation;
    }

    private static double calculateDistance(Point p1, Point p2) {
        int dx = p2.x - p1.x;
        int dy = p2.y - p1.y;
        return Math.sqrt(dx * dx + dy * dy);
    }
}