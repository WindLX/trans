#include "main_window.h"
#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    MainWindow w(argv[1]);
    w.show();
    return app.exec();
}