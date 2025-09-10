from omni.ui import Window
import omni.ui as ui
import omni
import omni.usd
from pxr import Usd, UsdGeom, Sdf, Gf
import omni.kit.commands
from omni.kit.notification_manager import post_notification

class MyWindow(Window):
    def __init__(self):
            super().__init__("My Test Window", width=400, height=500)
            self.visible = False
            
            self._count = ui.SimpleIntModel(0)
            self._text = ui.SimpleStringModel('Test String')

            self._usd_context = omni.usd.get_context()
            events = self._usd_context.get_stage_event_stream()
            self._stage_event_sub = events.create_subscription_to_pop(self._on_stage_event)
            self._stage : Usd.Stage = None
            
            self._build_view()
            self.reset()

    def _build_view(self):
        with self.frame:
            with ui.VStack(spacing=10, padding=10):
                self._label1 = ui.Label('')
                self._btn1   = ui.Button("Click Me!", clicked_fn=self.__clicked_fn)

                ui.Line(height=1)

                self._field  = ui.StringField(model=self._text)
                self._btn2   = ui.Button("Set Label content as Field", clicked_fn=self.__clicked_fn2)
                self._label2 = ui.Label('', model=self._text)

                ui.Line(height=1)

                self._btn3 = ui.Button('Make Xform', clicked_fn=self.__clicked_fn3)
                self._btn4 = ui.Button('Make Xform', clicked_fn=self.__clicked_fn4)
                
                ui.Line(height=1)

                ui.Label('Cube : ')

                with ui.HStack():
                    self._btn6 = ui.Button('-', clicked_fn=self.__clicked_fn5)
                    self._btn7 = ui.Button('Start / Reset',clicked_fn=self.__clicked_fn6)
                    self._btn8 = ui.Button('+', clicked_fn=self.__clicked_fn7)

    def _update_label1(self):
        self._label1.text = f"Clicked Count : {self._count.as_int}"

    def _update_label2(self):
        self._label2.text = self._text.as_string

    def reset(self):
        self._stage = self._usd_context.get_stage()
        self._count.set_value(0)
        self._text.set_value('Test String')
        self._update_label1()
        self._update_label2()

    def __clicked_fn(self):
        self._count.set_value(self._count.as_int + 1)
        self._update_label1()

    def __clicked_fn2(self):
        self._update_label2()

    def __clicked_fn3(self):
        xform : UsdGeom.Xformable = UsdGeom.Xform.Define(self._stage, Sdf.Path('/World/Xform_fn3'))

        trs = xform.GetTranslateOp()

        if trs is None:
            trs = xform.AddTranslateOp()
        ori = xform.GetOrientOp()

        if ori is None:
            ori = xform.AddOrientOp()
        sca = xform.GetScaleOp()

        if sca is None:    
            sca = xform.AddScaleOp()
        
        trs.Set(Gf.Vec3d(0, 0, 0))
        ori.Set(Gf.Quatf(1, 0, 0, 0))
        sca.Set(Gf.Vec3d(1, 1, 1))

    def __clicked_fn4(self):
        omni.kit.commands.execute(
            name='CreatePrimCommand',
            prim_type='Xform',
            prim_path='/World/Xform_fn4',
            select_new_prim=False
        )

    def __clicked_fn5(self):
        cube = self._stage.GetPrimAtPath('/World/Cube')
        if not cube.IsValid():
            post_notification('Need to Create Cube First!')
            return
        trs = cube.GetAttribute('xformOp:translate')
        trs.Set(trs.Get() + Gf.Vec3d(-0.5, 0, 0))

    def __clicked_fn6(self):
        omni.kit.commands.execute(
            name='CreatePrimCommand',
            prim_type='Cube',
            prim_path='/World/Cube',
            select_new_prim=False
        )
        cube = self._stage.GetPrimAtPath('/World/Cube')
        if not cube.IsValid():
            post_notification('Need to Create Cube First!')
            return
        trs = cube.GetAttribute('xformOp:translate')
        trs.Set(Gf.Vec3d(0, 0, 0))
        

    def __clicked_fn7(self):
        cube = self._stage.GetPrimAtPath('/World/Cube')
        if not cube.IsValid():
            post_notification('Need to Create Cube First!')
            return
        xformable = UsdGeom.Xformable(cube)
        for op in xformable.GetOrderedXformOps():
            if op.GetOpType() == UsdGeom.XformOp.TypeTranslate:
                trs_op = op
                break

        if trs_op is None:
            trs_op = xformable.AddTranslateOp()

        cur = trs_op.Get()
        if trs_op.GetPrecision() == UsdGeom.XformOp.PrecisionFloat:
            trs_op.Set(Gf.Vec3f(cur[0] + 0.5, cur[1], cur[2]))
        else:
            trs_op.Set(Gf.Vec3d(cur[0] + 0.5, cur[1], cur[2]))

    def _on_stage_event(self, event):
        if event.type == int(omni.usd.StageEventType.OPENED):
            self.visible = False