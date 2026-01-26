
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from datetime import datetime
import json
import os
from kivy.uix.recycleview import RecycleView
from kivy.uix.boxlayout import BoxLayout

Window.size = (360, 640)

KV = '''
ScreenManager:
    MenuScreen:
    SimpleInterestScreen:
    CompoundInterestScreen:
    RecordsScreen:

<MenuScreen>:
    name: "menu"
    BoxLayout:
        orientation: "vertical"
        padding: 30
        spacing: 20
        Label:
            text: "Interest Calculator"
            font_size: "26sp"
            bold: True
        Button:
            text: "Simple Interest"
            background_color: 0.2,0.5,1,1
            font_size: "18sp"
            on_release: app.root.current = "si"
        Button:
            text: "Compound Interest"
            background_color: 0.2,0.5,1,1
            font_size: "18sp"
            on_release: app.root.current = "ci"
        Button:
            text: "Saved Records"
            background_color: 0.2,0.5,1,1
            font_size: "18sp"
            on_release: app.root.current = "records"

<SimpleInterestScreen>:
    name: "si"
    BoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 10
        Label:
            text: "Simple Interest"
            font_size: "22sp"
            bold: True
            size_hint_y: None
            height: "30dp"
        TextInput:
            id: principal
            hint_text: "Principal Amount ₹"
            input_filter: 'float'
        TextInput:
            id: rate
            hint_text: "Interest Rate %"
            input_filter: 'float'
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 5
            ToggleButton:
                id: per_month
                text: "Per Month"
                group: "rate"
            ToggleButton:
                id: per_year
                text: "Per Year"
                group: "rate"
                state: "down"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 5
            ToggleButton:
                id: manual
                text: "Manual Duration"
                group: "duration_si"
                state: "down"
                on_release: root.show_manual()
            ToggleButton:
                id: by_date
                text: "By Dates"
                group: "duration_si"
                on_release: root.show_dates()
        BoxLayout:
            id: manual_box
            spacing: 5
            TextInput:
                id: years
                hint_text: "Years"
                input_filter: 'int'
            TextInput:
                id: months
                hint_text: "Months"
                input_filter: 'int'
            TextInput:
                id: days
                hint_text: "Days"
                input_filter: 'int'
        BoxLayout:
            id: date_box
            spacing: 5
            opacity: 0
            disabled: True
            TextInput:
                id: start_date
                hint_text: "Start Date (DD/MM/YYYY)"
            TextInput:
                id: end_date
                hint_text: "End Date (DD/MM/YYYY)"
        Button:
            text: "Calculate"
            background_color: 0.2,0.6,1,1
            on_release: root.calculate()
        Label:
            id: result
            text: ""
            font_size: "16sp"
        Button:
            text: "Back"
            on_release: app.root.current = "menu"

<CompoundInterestScreen>:
    name: "ci"
    BoxLayout:
        orientation: "vertical"
        padding: 15
        spacing: 10
        Label:
            text: "Compound Interest"
            font_size: "22sp"
            bold: True
            size_hint_y: None
            height: "35dp"
        TextInput:
            id: principal
            hint_text: "Principal Amount ₹"
            input_filter: 'float'
        TextInput:
            id: rate
            hint_text: "Interest Rate %"
            input_filter: 'float'
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 5
            ToggleButton:
                id: per_year
                text: "Per Year"
                group: "rate_ci"
                state: "down"
            ToggleButton:
                id: per_month
                text: "Per Month"
                group: "rate_ci"
        Label:
            text: "Compounding Frequency"
            size_hint_y: None
            height: "25dp"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 5
            ToggleButton:
                id: yearly
                text: "Yearly"
                group: "comp"
                state: "down"
            ToggleButton:
                id: half_yearly
                text: "Half-Yearly"
                group: "comp"
            ToggleButton:
                id: quarterly
                text: "Quarterly"
                group: "comp"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 5
            ToggleButton:
                id: monthly
                text: "Monthly"
                group: "comp"
            ToggleButton:
                id: daily
                text: "Daily"
                group: "comp"
        BoxLayout:
            size_hint_y: None
            height: "40dp"
            spacing: 5
            ToggleButton:
                id: manual
                text: "Manual Duration"
                group: "duration_ci"
                state: "down"
                on_release: root.show_manual_duration()
            ToggleButton:
                id: by_date
                text: "By Dates"
                group: "duration_ci"
                on_release: root.show_dates()
        BoxLayout:
            id: manual_box
            spacing: 5
            TextInput:
                id: years
                hint_text: "Years"
                input_filter: 'int'
            TextInput:
                id: months
                hint_text: "Months"
                input_filter: 'int'
            TextInput:
                id: days
                hint_text: "Days"
                input_filter: 'int'
        BoxLayout:
            id: date_box
            spacing: 5
            opacity: 0
            disabled: True
            TextInput:
                id: start_date
                hint_text: "Start Date DD/MM/YYYY"
            TextInput:
                id: end_date
                hint_text: "End Date DD/MM/YYYY"
        Button:
            text: "Calculate"
            background_color: 0.2,0.6,1,1
            on_release: root.calculate()
        Label:
            id: result
            text: ""
            font_size: "16sp"
        Button:
            text: "Back"
            on_release: app.root.current = "menu"

<RecordsScreen>:
    name: "records"
    BoxLayout:
        orientation: "vertical"
        padding: 20
        spacing: 15
        Label:
            text: "Calculation History"
            font_size: "24sp"
            bold: True
            size_hint_y: None
            height: "40dp"
        ScrollView:
            bar_width: 10
            RecordList:
                id: record_list
        BoxLayout:
            size_hint_y: None
            height: "50dp"
            spacing: 10
            Button:
                text: "Clear All"
                background_color: 1, 0.3, 0.3, 1
                on_release: root.clear_records()
            Button:
                text: "Back"
                background_color: 0.2,0.5,1,1
                on_release: app.root.current = "menu"

<RecordList@RecycleView>:
    viewclass: 'RecordItem'
    RecycleBoxLayout:
        default_size: None, dp(90)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        spacing: 5

<RecordItem@Label>:
    size_hint_y: None
    height: dp(90)
    padding: 15, 12
    text_size: self.size
    halign: 'left'
    valign: 'middle'
    font_size: '14sp'
    color: 0.1, 0.1, 0.1, 1
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.98, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12, 12, 12, 12]

'''

class MenuScreen(Screen):
    pass

class SimpleInterestScreen(Screen):
    def show_manual(self):
        self.ids.manual_box.opacity = 1
        self.ids.manual_box.disabled = False
        self.ids.date_box.opacity = 0
        self.ids.date_box.disabled = True

    def show_dates(self):
        self.ids.manual_box.opacity = 0
        self.ids.manual_box.disabled = True
        self.ids.date_box.opacity = 1
        self.ids.date_box.disabled = False

    def days_to_ymd(self, total_days):
        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        return int(years), int(months), int(days)

    def get_duration(self):
        if self.ids.manual.state == "down":
            try:
                y = int(self.ids.years.text or 0)
                m = int(self.ids.months.text or 0)
                d = int(self.ids.days.text or 0)
                total_days = y * 365 + m * 30 + d
                return total_days
            except:
                return 0
        else:
            start_text = self.ids.start_date.text.strip()
            end_text = self.ids.end_date.text.strip()
            if not start_text or not end_text:
                return 0
            try:
                s = datetime.strptime(start_text, "%d/%m/%Y")
                e = datetime.strptime(end_text, "%d/%m/%Y")
                if e > s:
                    return (e - s).days
                else:
                    return 0
            except ValueError:
                return 0

    def calculate(self):
        try:
            P = float(self.ids.principal.text or 0)
            R = float(self.ids.rate.text or 0)
            total_days = self.get_duration()

            if total_days <= 0:
                self.ids.result.text = "Invalid duration. Enter valid dates."
                return

            if P <= 0 or R < 0:
                self.ids.result.text = "Invalid principal or rate"
                return

            if self.ids.per_month.state == "down":
                R = R * 12

            T_decimal = total_days / 365
            interest = (P * R * T_decimal) / 100
            total = P + interest

            years, months, days = self.days_to_ymd(total_days)
            
            # Save to records
            App.get_running_app().save_record("Simple", P, R, (years, months, days), interest, total)
            
            self.ids.result.text = (
                f"Duration:\n"
                f"│ Years │ Months │ Days  │\n"
                f"│  {years:4} │  {months:5} │ {days:4}  │\n"
                f"Interest: ₹{interest:.2f}\n"
                f"Total Amount: ₹{total:.2f}"
            )
        except Exception as e:
            self.ids.result.text = "Invalid input. Check values."

class CompoundInterestScreen(Screen):
    def show_manual_duration(self):
        self.ids.manual_box.opacity = 1
        self.ids.manual_box.disabled = False
        self.ids.date_box.opacity = 0
        self.ids.date_box.disabled = True

    def show_dates(self):
        self.ids.manual_box.opacity = 0
        self.ids.manual_box.disabled = True
        self.ids.date_box.opacity = 1
        self.ids.date_box.disabled = False

    def days_to_ymd(self, total_days):
        years = total_days // 365
        remaining_days = total_days % 365
        months = remaining_days // 30
        days = remaining_days % 30
        return int(years), int(months), int(days)

    def get_duration(self):
        if self.ids.manual.state == "down":
            try:
                y = int(self.ids.years.text or 0)
                m = int(self.ids.months.text or 0)
                d = int(self.ids.days.text or 0)
                total_days = y * 365 + m * 30 + d
                return total_days
            except:
                return 0
        else:
            start_text = self.ids.start_date.text.strip()
            end_text = self.ids.end_date.text.strip()
            if not start_text or not end_text:
                return 0
            try:
                s = datetime.strptime(start_text, "%d/%m/%Y")
                e = datetime.strptime(end_text, "%d/%m/%Y")
                if e > s:
                    return (e - s).days
                else:
                    return 0
            except ValueError:
                return 0

    def get_frequency(self):
        if self.ids.yearly.state == "down":
            return 1
        elif self.ids.half_yearly.state == "down":
            return 2
        elif self.ids.quarterly.state == "down":
            return 4
        elif self.ids.monthly.state == "down":
            return 12
        elif self.ids.daily.state == "down":
            return 365
        return 1

    def calculate(self):
        try:
            P = float(self.ids.principal.text or 0)
            R = float(self.ids.rate.text or 0)

            if P <= 0 or R < 0:
                self.ids.result.text = "Invalid principal or rate"
                return

            if self.ids.per_month.state == "down":
                R = R * 12

            n = self.get_frequency()
            total_days = self.get_duration()
            
            if total_days <= 0:
                self.ids.result.text = "Invalid duration. Check inputs."
                return

            T_decimal = total_days / 365
            amount = P * (1 + R/(100*n)) ** (n * T_decimal)
            interest = amount - P

            years, months, days = self.days_to_ymd(total_days)
            
            # Save to records
            App.get_running_app().save_record("Compound", P, R, (years, months, days), interest, amount)
            
            self.ids.result.text = (
                f"Duration:\n"
                f"│ Years │ Months │ Days  │\n"
                f"│  {years:4} │  {months:5} │ {days:4}  │\n"
                f"Frequency: {n}x/Year\n"
                f"Interest: ₹{interest:.2f}\n"
                f"Total Amount: ₹{amount:.2f}"
            )
        except Exception as e:
            self.ids.result.text = "Invalid input. Check values."

class RecordList(RecycleView):
    pass

class RecordItem(BoxLayout):
    pass

class RecordsScreen(Screen):
    def on_enter(self):
        app = App.get_running_app()
        self.ids.record_list.data = []
        
        if not app.records:
            # Show empty state
            self.ids.record_list.data = [{
                'text': '[b][color=999999]No calculations yet.\nStart calculating to see history![/color][/b]'
            }]
            return
        
        for record in app.records:
            self.ids.record_list.data.append({
                'text': f"[b]{record['timestamp']}[/b] - [color=0.2,0.5,1]{record['type']}[/color]\n"
                       f"P: {record['principal']} | R: {record['rate']} | D: {record['duration']}\n"
                       f"[color=0.2,0.6,1]I: {record['interest']} | Total: {record['total']}[/color]"
            })

    def clear_records(self):
        App.get_running_app().clear_records()
        self.ids.record_list.data = [{
            'text': '[b][color=999999]No calculations yet.\nStart calculating to see history![/color][/b]'
        }]


    def clear_records(self):
        App.get_running_app().clear_records()
        self.ids.record_list.data = []

class InterestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.records_file = "interest_records.json"
        self.records = self.load_records()
    
    def load_records(self):
        if os.path.exists(self.records_file):
            try:
                with open(self.records_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_record(self, calc_type, principal, rate, duration_ymd, interest, total):
        record = {
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M"),
            'type': calc_type,
            'principal': f"₹{principal:.2f}",
            'rate': f"{rate}%",
            'duration': f"{duration_ymd[0]}Y {duration_ymd[1]}M {duration_ymd[2]}D",
            'interest': f"₹{interest:.2f}",
            'total': f"₹{total:.2f}"
        }
        self.records.insert(0, record)
        if len(self.records) > 50:
            self.records = self.records[:50]
        self.save_records()
    
    def save_records(self):
        with open(self.records_file, 'w') as f:
            json.dump(self.records, f, indent=2)
    
    def clear_records(self):
        self.records = []
        self.save_records()
    
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    InterestApp().run()
