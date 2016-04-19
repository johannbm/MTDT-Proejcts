package sample;

import javafx.application.Platform;
import javafx.beans.property.SimpleStringProperty;

import java.util.ArrayList;

/**
 * Created by Johannes on 18.10.2015.
 */
public class SimulateRun implements Runnable{

    private Controller controller;
    private Board currentBoard;
    private ArrayList<Board> previousBoards;
    private SimpleStringProperty moveCounter;
    private SimpleStringProperty currentEvaluationScore;
    private int delay;
    public static int moveCounterNumber;

    public SimulateRun(Board board, Controller controller,
                       SimpleStringProperty moveCounter,
                       SimpleStringProperty currentEvaluationScore,
                       ArrayList<Board> previousBoards, int delay) {
        this.previousBoards = previousBoards;
        currentBoard = board;
        this.moveCounter = moveCounter;
        this.delay = delay;
        this.currentEvaluationScore = currentEvaluationScore;
        this.controller = controller;
        previousBoards.add(currentBoard.getCopy());
    }

    @Override
    public void run() {
        while (!currentBoard.isGameOver()) {
            simulateOneGameLoop();

            try {
                Thread.sleep(delay);
            } catch (InterruptedException e) {
                break;
            }
        }
    }

    public void simulateOneGameLoop() {
        moveCounterNumber++;

        Direction move = AI.alphaBetaPruning(currentBoard, 3, 3, -100000, 100000, true);
        currentBoard.move(move);

        if (Util.compareBoards(previousBoards.get(previousBoards.size()-1).getBoard(), currentBoard.getBoard())) {
            currentBoard.spawnTile();
        }
        previousBoards.add(currentBoard.getCopy());
        Platform.runLater(() -> {
            controller.paintBoard(currentBoard.getBoard());
            moveCounter.set("Move #" + Integer.toString(moveCounterNumber));
            currentEvaluationScore.set("Evaluation: " + String.format("%.2f", Evaluation.evaluate(currentBoard)));
        });
    }
}
