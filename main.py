from nicegui import ui, app

app.add_static_files('/assets', 'assets')
ui.query('.nicegui-content').classes('p-0 gap-0', remove='q-pa-md')
app.native.window_args['title'] = 'KokoSpeak'

ui.add_css("""
.no-resize { resize: none !important; }
""")

with ui.row().classes('relative justify-center h-screen w-full flex flex-col bg-cover bg-center bg-no-repeat overflow-hidden') \
        .style('background-image: url(/assets/backgroundImage.gif)'):
    ui.element('div').classes('backdrop-grayscale')
    ui.element('div').classes('absolute inset-0 bg-black/15 backdrop-blur-md')

    with ui.column().classes('relative z-10 h-full w-full flex flex-col justify-between m-5'):
        with ui.element('div').classes('header'):
            ui.label('KokoSpeak').classes('text-shadow-sm sm:text-3xl md:text-5xl font-bold text-white')
            ui.label('Using open-sourced AI, Kokoro').classes('text-shadow-md text-white text-xl md:text-2xl font-semibold')

        with ui.element('div').classes('w-[91vw] justify-center flex flex-1 pb-4'):
            with ui.element('div').classes('bg-black/75 rounded-xl backdrop-blur-md p-4 w-full'):
                with ui.element('div').classes('flex flex-1 h-full'):
                    with ui.element('div').classes('flex-1 flex flex-col p-4 gap-3 min-h-0'):
                        ui.label('Prompt / Text').classes('text-white font-semibold text-2xl')

                        with ui.scroll_area().classes('dark color=purple-12 w-full h-40 rounded-md bg-black/30 p-2'):
                            i = ui.textarea(placeholder='Type something...') \
                                .props('dark clearable color=purple-12 autogrow input-class="no-resize text-white" input-style="overflow:hidden"') \
                                .classes('w-full')

                    with ui.element('div').classes('flex-1 flex flex-col p-4 gap-3 overflow-auto'):
                        ui.label('Audio Preview').classes('text-white font-semibold text-2xl')

ui.run(native=True, reload=False)
