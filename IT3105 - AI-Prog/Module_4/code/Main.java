package sample;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.input.KeyCode;
import javafx.stage.Stage;

import java.util.ArrayList;

public class Main extends Application {

    public ArrayList<Board> previousBoards;
    public Board currentBoard;

    Controller controller;
    @Override
    public void start(Stage primaryStage) throws Exception{
        previousBoards = new ArrayList<>();
        primaryStage.setTitle("2048");

        FXMLLoader fxmlLoader = new FXMLLoader();
        Parent root = fxmlLoader.load(getClass().getResource("gameLayout.fxml").openStream());
        controller = fxmlLoader.getController();

        currentBoard = new Board();
        previousBoards.add(currentBoard.getCopy());
        controller.board = currentBoard;
        controller.main = this;

        Scene scene = new Scene(root, 800, 600);

        scene.setOnKeyReleased(event -> {
            if (event.getCode() == KeyCode.UP || event.getCode() == KeyCode.DOWN || event.getCode() == KeyCode.RIGHT || event.getCode() == KeyCode.LEFT) {
                if (event.getCode() == KeyCode.UP)
                    currentBoard.move(Direction.UP);
                else if (event.getCode() == KeyCode.DOWN)
                    currentBoard.move(Direction.DOWN);
                else if (event.getCode() == KeyCode.RIGHT)
                    currentBoard.move(Direction.RIGHT);
                else if (event.getCode() == KeyCode.LEFT)
                    currentBoard.move(Direction.LEFT);


                if (previousBoards.size() > 0) {
                    if (previousBoards.size() > 1) {
                        if (Util.compareBoards(previousBoards.get(previousBoards.size() - 1).getBoard(), currentBoard.getBoard())) {
                            currentBoard.spawnTile();
                            System.out.println("a");
                        }
                    } else {
                        //currentBoard.spawnTile();
                        System.out.println("b");
                    }
                } else {
                    currentBoard.spawnTile();
                    System.out.println("c");
                }

                previousBoards.add(currentBoard.getCopy());
                controller.paintBoard(currentBoard.getBoard());
            }
        });
        primaryStage.setScene(scene);
        primaryStage.show();

        controller.initialize();
        currentBoard.spawnTile();
        controller.paintBoard(currentBoard.getBoard());
    }


    public void undo() {
        if (previousBoards.size() > 1) {
            currentBoard = previousBoards.get(previousBoards.size() - 2).getCopy();
            previousBoards.remove(previousBoards.size() - 1);
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
