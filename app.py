import os
import requests
import json
from flask import Flask, request

app = Flask(__name__)

VERIFY_TOKEN = "koshri_webhook_2026"
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")


@app.route("/api/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Forbidden", 403


@app.route("/api/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)

    print("\n================ WEBHOOK EVENT ================")
    print(json.dumps(data, indent=4, ensure_ascii=False))
    print("================================================\n")

    try:
        entry = data.get("entry", [])

        for entry_item in entry:
            changes = entry_item.get("changes", [])

            for change in changes:
                value = change.get("value", {})

                # =========================
                # Incoming messages
                # =========================
                messages = value.get("messages", [])

                if messages:
                    print(">>> INCOMING MESSAGE")

                    for message in messages:
                        print("Message ID:", message.get("id"))
                        print("From:", message.get("from"))
                        print("Type:", message.get("type"))

                # =========================
                # Outgoing message statuses
                # =========================
                statuses = value.get("statuses", [])

                if statuses:
                    print(">>> WHATSAPP MESSAGE STATUS")

                    for status in statuses:
                        print("Message ID:", status.get("id"))
                        print("Status:", status.get("status"))
                        print("Recipient:", status.get("recipient_id"))
                        print("Timestamp:", status.get("timestamp"))

                        if status.get("errors"):
                            print("ERRORS:")
                            print(
                                json.dumps(
                                    status.get("errors"),
                                    indent=4,
                                    ensure_ascii=False
                                )
                            )

    except Exception as e:
        print("Webhook processing error:", str(e))

    return "OK", 200

@app.route("/privacy-policy", methods=["GET"])
def privacy_policy():
    return """
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>سياسة الخصوصية - الغباشي كشري و حلواني</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.8;
                max-width: 900px;
                margin: 40px auto;
                padding: 20px;
                color: #222;
                background: #fff;
            }

            h1, h2 {
                color: #333;
            }

            h1 {
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
            }

            .updated {
                color: #777;
                font-size: 14px;
            }
        </style>
    </head>

    <body>

        <h1>سياسة الخصوصية</h1>

        <p class="updated">آخر تحديث: سبتمبر 2026</p>

        <p>
            تحترم شركة <strong>الغباشي كشري و حلواني</strong> خصوصية عملائها
            وتهتم بحماية البيانات الشخصية التي يتم التعامل معها من خلال خدماتنا.
        </p>

        <h2>البيانات التي قد نقوم بجمعها</h2>

        <p>
            قد نقوم بجمع بعض البيانات التي يقدمها العميل عند التواصل معنا،
            مثل الاسم ورقم الهاتف ومحتوى الرسائل، وذلك بهدف تقديم خدمة العملاء
            والتواصل مع العملاء وإرسال المعلومات والعروض المتعلقة بخدماتنا.
        </p>

        <h2>كيفية استخدام البيانات</h2>

        <ul>
            <li>التواصل مع العملاء والرد على استفساراتهم.</li>
            <li>تقديم خدمات الطلبات وخدمة العملاء.</li>
            <li>إرسال العروض والتحديثات المتعلقة بخدمات الغباشي كشري و حلواني.</li>
            <li>تحسين جودة الخدمات وتجربة العملاء.</li>
        </ul>

        <h2>مشاركة البيانات</h2>

        <p>
            لا نقوم ببيع أو تأجير البيانات الشخصية للعملاء.
            وقد يتم التعامل مع البيانات من خلال مزودي الخدمات التقنية
            الضروريين لتشغيل خدمات التواصل، بما في ذلك خدمات WhatsApp وMeta،
            وفقًا للسياسات والأنظمة المعمول بها.
        </p>

        <h2>حماية البيانات</h2>

        <p>
            نتخذ إجراءات مناسبة للمساعدة في حماية البيانات الشخصية من الوصول
            غير المصرح به أو الاستخدام أو التغيير أو الكشف غير المصرح به.
        </p>

        <h2>الاحتفاظ بالبيانات</h2>

        <p>
            نحتفظ بالبيانات فقط بالقدر اللازم للأغراض التي تم جمعها من أجلها
            أو حسبما تقتضي المتطلبات القانونية والتشغيلية.
        </p>

        <h2>حقوق العميل</h2>

        <p>
            يمكن للعميل طلب معرفة البيانات المتعلقة به أو طلب تصحيحها أو
            حذفها، حسبما تسمح به القوانين والأنظمة المعمول بها.
        </p>

        <h2>التواصل معنا</h2>

        <p>
            إذا كان لديك أي استفسار يتعلق بسياسة الخصوصية أو طريقة استخدام
            بياناتك، يمكنك التواصل مع إدارة الغباشي كشري و حلواني من خلال
            قنوات التواصل الرسمية الخاصة بنا.
        </p>

        <h2>تحديث سياسة الخصوصية</h2>

        <p>
            قد نقوم بتحديث سياسة الخصوصية من وقت لآخر. وسيتم نشر أي تحديثات
            على هذه الصفحة.
        </p>

    </body>
    </html>
    """
