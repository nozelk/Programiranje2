public class Main {
    public static void main(String[] args) {
        Order order = new Order();

        Restaurant restaurant = new Restaurant("McDonalds");
        order.addItem(new Item("Big Mac", 3.9, restaurant));
        order.addItem(new Item("Hamburger", 1.7, restaurant));
        order.addItem(new Item("Fries", 1.7, restaurant));

        restaurant = new Restaurant("HoodBurger");
        order.addItem(new Item("Le Brie", 7.3, restaurant));
        order.addItem(new Item("Krompirček", 3.7, restaurant));

        System.out.println(order);
    }
}