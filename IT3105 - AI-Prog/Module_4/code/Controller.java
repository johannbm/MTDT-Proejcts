package sample;

import javafx.beans.property.SimpleStringProperty;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;

import java.util.*;

public class Controller {

    public AnchorPane parentPane;

    public Board board;

    public Main main;

    public boolean aiIsRunning;
    @FXML
    private Button runAIButton;
    @FXML
    private Button undo;
    @FXML
    private Button hint;
    @FXML
    private Label moveCounterLabel;
    @FXML
    private Label evaluationScoreLabel;
    @FXML
    private TextField delay;

    @FXML
    private Label label_00;
    @FXML
    private Label label_01;
    @FXML
    private Label label_02;
    @FXML
    private Label label_03;
    @FXML
    private Label label_10;
    @FXML
    private Label label_11;
    @FXML
    private Label label_12;
    @FXML
    private Label label_13;
    @FXML
    private Label label_20;
    @FXML
    private Label label_21;
    @FXML
    private Label label_22;
    @FXML
    private Label label_23;
    @FXML
    private Label label_30;
    @FXML
    private Label label_31;
    @FXML
    private Label label_32;
    @FXML
    private Label label_33;

    private ArrayList<ArrayList<Label>> labels;

    public void initialize() {

        labels = new ArrayList<>();
        ArrayList<Label> l0 = new ArrayList<>();
        l0.add(label_00);
        l0.add(label_01);
        l0.add(label_02);
        l0.add(label_03);
        ArrayList<Label> l1 = new ArrayList<>();
        l1.add(label_10);
        l1.add(label_11);
        l1.add(label_12);
        l1.add(label_13);
        ArrayList<Label> l2 = new ArrayList<>();
        l2.add(label_20);
        l2.add(label_21);
        l2.add(label_22);
        l2.add(label_23);
        ArrayList<Label> l3 = new ArrayList<>();
        l3.add(label_30);
        l3.add(label_31);
        l3.add(label_32);
        l3.add(label_33);

        labels.add(l0);
        labels.add(l1);
        labels.add(l2);
        labels.add(l3);
    }

    public void paintBoard(Integer[][] board) {
        for (int x = 0; x < board.length; x++) {
            for (int y = 0; y < board.length; y++) {
                updateTile(x,y,board[x][y]);
            }
        }
    }

    private void updateTile(int x, int y, int newValue) {
        Label l = labels.get(x).get(y);
        l.setText((newValue == 0) ? "" : String.valueOf(newValue));
        l.setStyle(getColor(newValue));
    }

    private String getColor(int value) {
        switch (value) {
            case 2:
                return "-fx-background-color: #eee4da;";
            case 4:
                return "-fx-background-color: #ede0c8;";
            case 8:
                return "-fx-background-color: #f2b179;";
            case 16:
                return "-fx-background-color: #f59563;";
            case 32:
                return "-fx-background-color: #f67c5f;";
            case 64:
                return "-fx-background-color: #f65e3b;";
            case 128:
                return "-fx-background-color: #edcf72;";
            case 256:
                return "-fx-background-color: #edcc61;";
            case 512:
                return "-fx-background-color: #edc850;";
            case 1024:
                return "-fx-background-color: #edc53f;";
            case 2048:
                return "-fx-background-color: #edc53f;";
            case 4096:
                return "-fx-background-color: #edc22e;";
        }
        return "";
    }


    public void undoMove(ActionEvent actionEvent) {
        main.undo();
        paintBoard(main.currentBoard.getBoard());
    }

    Thread currentAiThread;

    public void runAI(ActionEvent actionEvent) {
        if (!aiIsRunning) {
            runAIButton.setText("Stop AI");
            undo.setDisable(true);
            hint.setDisable(true);
            SimpleStringProperty moveCounter = new SimpleStringProperty();
            SimpleStringProperty evaluationScore = new SimpleStringProperty();
            moveCounterLabel.textProperty().bind(moveCounter);
            evaluationScoreLabel.textProperty().bind(evaluationScore);
            SimulateRun aiRun = new SimulateRun(main.currentBoard, this, moveCounter,
                    evaluationScore, main.previousBoards, Integer.parseInt(delay.getText()));
            currentAiThread = new Thread(aiRun);
            currentAiThread.start();
        } else {
            currentAiThread.interrupt();

            runAIButton.setText("Start AI");
            undo.setDisable(false);
            hint.setDisable(false);
        }
        aiIsRunning = !aiIsRunning;
    }
}
