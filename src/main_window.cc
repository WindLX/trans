#include "main_window.h"

MainWindow::MainWindow(const char *trans_path, QWidget *parent)
    : QMainWindow(parent), ui(new Ui::MainWindow)
{
    this->ui->setupUi(this);
    connect(ui->transButton, SIGNAL(clicked()), this, SLOT(on_transButton_clicked()));
    connect(ui->clearButton, SIGNAL(clicked()), this, SLOT(on_clearButton_clicked()));

    this->trans_process = new QProcess(this);
    this->trans_process->setWorkingDirectory(trans_path);
    this->trans_process->setProcessChannelMode(QProcess::MergedChannels);
    this->trans_process->setProgram("./trans.sh");
    this->trans_process->setArguments(QStringList() << trans_path);
    this->trans_process->start();
    this->trans_process->waitForStarted();
}

MainWindow::~MainWindow()
{
    this->trans_process->kill();
    this->trans_process->waitForFinished();
    delete this->ui;
}

void MainWindow::on_transButton_clicked()
{
    auto raw_text = this->ui->inputEditor->toPlainText();
    if (raw_text == "EXIT")
    {
        raw_text = "";
        this->ui->inputEditor->clear();
    }
    if (raw_text != "")
    {
        auto clean_text = raw_text.simplified();
        clean_text.append("\r\n");
        this->trans_process->write(clean_text.toLocal8Bit());
        this->trans_process->waitForReadyRead();

        auto response = QString::fromLocal8Bit(this->trans_process->readAllStandardOutput());
        this->ui->outputEditor->setText(response);
    }
}

void MainWindow::on_clearButton_clicked()
{
    this->ui->outputEditor->clear();
    this->ui->inputEditor->clear();
}