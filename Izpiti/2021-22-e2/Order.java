import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

class Order {
   private List<Item> items;

    public Order() {
        items = new ArrayList<>();
    }

    public void addItem(Item item) {
        items.add(item);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        Map<Restaurant, List<Item>> restaurantItemsMap = new HashMap<>();

        // Group items by restaurant
        for (Item item : items) {
            List<Item> restaurantItems = restaurantItemsMap.getOrDefault(item.getRestaurant(), new ArrayList<>());
            restaurantItems.add(item);
            restaurantItemsMap.put(item.getRestaurant(), restaurantItems);
        }

        // Calculate total price and print each restaurant's items
        double totalPrice = 0.0;
        for (Restaurant restaurant : restaurantItemsMap.keySet()) {
            List<Item> restaurantItems = restaurantItemsMap.get(restaurant);

            sb.append(restaurant.getName()).append(":\t\t");
            sb.append(getRestaurantItemsString(restaurantItems)).append("\n");

            double restaurantTotalPrice = calculateTotalPrice(restaurantItems);
            sb.append("\t\t\t\t").append(restaurantTotalPrice).append("€\n");

            totalPrice += restaurantTotalPrice;
        }

        sb.append("\t\t\t\tSkupaj: ").append(totalPrice).append("€");

        return sb.toString();
    }

    private String getRestaurantItemsString(List<Item> restaurantItems) {
        StringBuilder sb = new StringBuilder();
        for (Item item : restaurantItems) {
            sb.append(item.getName()).append(", ");
        }
        sb.delete(sb.length() - 2, sb.length()); // Remove the last comma and space
        return sb.toString();
    }

    private double calculateTotalPrice(List<Item> items) {
        double totalPrice = 0.0;
        for (Item item : items) {
            totalPrice += item.getPrice();
        }
        return totalPrice;
    }
}
