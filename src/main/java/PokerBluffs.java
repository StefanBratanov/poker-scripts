import java.util.Scanner;

public class PokerBluffs {

    public static void main(String[] args) {
        var potSize = 100.0;

        Scanner scanner = new Scanner(System.in);

        System.out.printf("Please select a bet size for the current " +
                "pot %f %n", potSize);
        var bet = scanner.nextInt();

        double potOdds = potSize / bet;

        var percentageToWork = 100.0 / (potOdds + 1.0);

        System.out.printf("Opponent needs to fold more than %f percent for your bluff" +
                        "to be profitable %n",
                percentageToWork);
    }
}
