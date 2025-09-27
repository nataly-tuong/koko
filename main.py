from nicegui import ui, app

app.add_static_files('/assets', 'assets')
app.native.window_args['title'] = 'KokoSpeak'

ui.add_css(".no-resize { resize: none !important; }")

with ui.element('div').classes('fixed inset-0 p-5 overflow-hidden bg-cover bg-center bg-no-repeat') \
        .style('background-image: url(/assets/backgroundImage.gif)'):
    ui.element('div').classes('absolute inset-0')
    ui.element('div').classes('absolute inset-0 bg-black/15 backdrop-blur md:backdrop-blur-md lg:backdrop-blur-xl')

    with ui.element('div').classes('relative z-10 flex flex-col w-full h-full'):
        with ui.element('div').classes('w-full pt-3 pb-3'):
            ui.label('KokoSpeak').classes('text-white font-bold text-2xl sm:text-5xl md:text-6xl lg:text-8xl')
            ui.label('Using open-sourced AI, Kokoro').classes('text-white/90 font-semibold text-xs sm:text-lg md:text-xl')

        with ui.element('div').classes('flex-1 w-full flex'):
            with ui.element('div').classes('bg-blend-multiply bg-black/60 rounded-xl backdrop-blur-md w-full p-5 gap-5 flex-1 flex min-h-0'):
                with ui.element('div').classes('flex flex-1 min-h-0 flex-col sm:flex-row gap-4'):
                    with ui.element('div').classes('flex-1 flex min-h-0 flex-col gap-3'):
                        ui.label('Prompt / Text').classes('text-white font-semibold text-base sm:text-2xl')
                        with ui.scroll_area().classes('flex-1 w-full rounded-md bg-black/90 p-2 min-h-0'):
                            ui.textarea(placeholder='Type something...') \
                                .props('dark clearable color=purple-12 autogrow input-class="no-resize text-white" input-style="overflow:hidden"') \
                                .classes('w-full')
                        with ui.element('div').classes('flex gap-3 w-full'):
                            ui.button('Generate').props('color=black/90').classes('flex-1')
                            ui.button('Clear').props('color=black/90').classes('flex-1')
                    with ui.element('div').classes('flex-1 flex min-h-0 flex-col gap-3'):
                        ui.label('Audio Preview').classes('text-white font-semibold text-base sm:text-2xl')

ui.run(native=True, reload=False)
