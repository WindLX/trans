#ifndef MAIN_H
#define MAIN_H

#include "../ui/ui_main_window.h"
#include <QProcess>
#include <QMainWindow>

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(const char *trans_path, QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_transButton_clicked();
    void on_clearButton_clicked();

private:
    Ui::MainWindow *ui;
    QProcess *trans_process;
};

#endif