#!/usr/bin/python
# -*- coding: utf-8 -*-
from set_screen import Gui
import parameters as para
from event_rec_gui import Cont_rec
from emr_rec_gui import Emr_rec


gui = Gui()
cont = Cont_rec()
emr = Emr_rec()


if __name__ == '__main__':

    try:
        while True:

            gui.select_cam()
            if para.event == "next":
                gui.set_resolution()            
            elif para.event == "init":
                continue
            else:
                break

            if para.event == "next":
                gui.mode_select()
            else:
                break

            if para.event == "cont":
                gui.input_totaltime()

                if para.event == "next":
                    gui.select_startmethod()
                elif para.event == "init":
                    continue
                else:
                    break

                if para.event == "rapid":
                    gui.set_rapid_start()
                elif para.event == "spec":
                    gui.set_spec_start()
                elif para.event == "init":
                    continue
                else:
                    break

                if para.event == "next":
                    gui.start_eventrec()
                elif para.event == "init":
                    continue
                else:
                    break

                if para.event == "next":
                    rec_flag = cont.exec()
                    print(rec_flag)
                elif para.event == "init":
                    continue
                #else:
                #    break


            elif para.event == "emr":
                gui.set_sesitivity()

                if para.event == "next":
                    gui.start_ermrec()
                elif para.event == "init":
                    continue
                else:
                    break

                if para.event == "next":
                    rec_flag = emr.exec()
                else: #elif para.event == "init":
                    continue
                #else:
                #    break

            elif para.event == "init" or rec_flag == True:
                continue
            else:
                break

    except KeyboardInterrupt:
        gui.set_resolution()
