
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Buttons used

home_button = [
    [InlineKeyboardButton("🌏 Source", "source_btn"),
     InlineKeyboardButton("⬇️  Fr. Id", "from_btn"),
     InlineKeyboardButton("❓ Help", url="https://telegra.ph/Clonebot-UI-Help-05-30")],
    [InlineKeyboardButton("🎯 Target", "target_btn"),
     InlineKeyboardButton("⬆️  To Id", "up_to_btn"),
     InlineKeyboardButton("Types  ➡", "types_btn")],
    [InlineKeyboardButton("Delayed", "delay_btn"),
     InlineKeyboardButton("Caption", "caption_btn"),
     InlineKeyboardButton("FNAC", "f_caption_btn")],
    [InlineKeyboardButton("🔎️  View", "view_btn"),
     InlineKeyboardButton("🚮  Reset", "rst_btn"),
     InlineKeyboardButton("❌  Close", "close_btn")],
    [InlineKeyboardButton("🚦 Clone Medias 🚦", "clone_btn")]
]


start_button = [
    [InlineKeyboardButton("🏅 GitHub 🏅", url="github.com/m4mallu/clonebot"),
     InlineKeyboardButton("⚙️Settings ⚙", "start_btn")]
]


types_button = [
    [InlineKeyboardButton(" ⏺ Docs", "docs_btn"),
     InlineKeyboardButton(" ⏺ Video", "video_btn"),
     InlineKeyboardButton(" ⏺ Audio", "audio_btn")],
    [InlineKeyboardButton(" ⏺ Photo", "photo_btn"),
     InlineKeyboardButton(" ⏺ Voice", "voice_btn"),
     InlineKeyboardButton("⚙️ View", "view_types")],
    [InlineKeyboardButton("⬅️ Back", "start_btn")]
]


stop_button = [
    [InlineKeyboardButton("🚫 STOP 🚫", "stop_clone")]
]


finished_button = [
    [InlineKeyboardButton("🏠  HOME", "start_btn"),
     InlineKeyboardButton("❌  CLOSE", "close_btn")]
]


terminate_btn = [
    [InlineKeyboardButton("🧸 Updates", url="https://github.com/m4mallu/clonebot-ui"),
     InlineKeyboardButton("❓ Usage", url="https://telegra.ph/Clonebot-UI-Help-05-30")],
    [InlineKeyboardButton("🚫 Terminate", "terminate_btn"),
     InlineKeyboardButton("🏠 Home", "start_btn")]
]

indexing_skip_button = [
        [
            InlineKeyboardButton("🕹 Skip", "index_skip_btn")
        ]
    ]

purging_skip_button = [
        [
            InlineKeyboardButton("🕹 Skip", "purge_skip_btn")
        ]
    ]

purge_button = [
    [
        InlineKeyboardButton("Nop", "purge_no_btn"),
        InlineKeyboardButton("Purge it 👍", "purge_yes_btn")
    ]
]

# markups used

reply_markup_purge = InlineKeyboardMarkup(purge_button)

reply_markup_skip_index = InlineKeyboardMarkup(indexing_skip_button)

reply_markup_skip_purge = InlineKeyboardMarkup(purging_skip_button)

reply_markup_stop = InlineKeyboardMarkup(stop_button)

reply_markup_home = InlineKeyboardMarkup(home_button)

reply_markup_start = InlineKeyboardMarkup(start_button)

reply_markup_terminate = InlineKeyboardMarkup(terminate_btn)

reply_markup_finished = InlineKeyboardMarkup(finished_button)

reply_markup_types_button = InlineKeyboardMarkup(types_button)
