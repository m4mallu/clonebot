
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


home_button = [
    [
        InlineKeyboardButton("🌏 Source", "source_btn"),
        InlineKeyboardButton("⬇️  Fr. Id", "from_btn"),
        InlineKeyboardButton("❓ Help", url="https://bit.ly/3z2jquF")
    ],
    [
        InlineKeyboardButton("🎯 Target", "target_btn"),
        InlineKeyboardButton("⬆️  To Id", "up_to_btn"),
        InlineKeyboardButton("Types  ➡", "types_btn")
    ],
    [
        InlineKeyboardButton("Delayed", "delay_btn"),
        InlineKeyboardButton("Caption", "caption_btn"),
        InlineKeyboardButton("FNAC", "f_caption_btn")
    ],
    [
        InlineKeyboardButton("🔎️  View", "view_btn"),
        InlineKeyboardButton("✍️ CC", "cust_captn_btn"),
        InlineKeyboardButton("❌  Close", "close_btn")
    ],
    [
        InlineKeyboardButton("🗑  Reset", "rst_btn"),
        InlineKeyboardButton("🔄  Restart", "restart_btn")
    ],
    [
        InlineKeyboardButton("🚦 Clone Messages 🚦", "clone_btn")
    ]
]


start_button = [
    [
        InlineKeyboardButton("🏅 GitHub 🏅", url="github.com/m4mallu/clonebot"),
        InlineKeyboardButton("⚙️ Settings ⚙", "start_btn")
    ]
]


types_button = [
    [
        InlineKeyboardButton("Docs ✅", "docs_yes_btn"),
        InlineKeyboardButton("Video ✅", "video_yes_btn"),
        InlineKeyboardButton("Audio ✅", "audio_yes_btn")
    ],
    [
        InlineKeyboardButton("Photo ✅", "photo_yes_btn"),
        InlineKeyboardButton("Voice ✅", "voice_yes_btn"),
        InlineKeyboardButton("Text ✅", "text_yes_btn")
    ],
    [
        InlineKeyboardButton("⚙️ View", "view_types"),
        InlineKeyboardButton("⬅️ Back", "start_btn")
    ]
]


stop_button = [
    [
        InlineKeyboardButton("🚫 STOP 🚫", "stop_clone")
    ]
]


finished_button = [
    [
        InlineKeyboardButton("Home", "start_btn"),
        InlineKeyboardButton("Close", "close_btn")
    ]
]


close_button = [
    [
        InlineKeyboardButton("Delete", "close_btn"),
        InlineKeyboardButton("Close", "clear_btn")
    ]
]


terminate_btn = [
    [
        InlineKeyboardButton("🧸 Updates", url="https://github.com/m4mallu/clonebot"),
        InlineKeyboardButton("❓ Usage", url="https://bit.ly/3z2jquF")
    ],
    [
        InlineKeyboardButton("🚫 Terminate", "terminate_btn"),
        InlineKeyboardButton("🏠 Home", "start_btn")
    ]
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

caption_cnf_button = [
    [
        InlineKeyboardButton("YES ✅", "capt_cnf_yes_btn"),
        InlineKeyboardButton("NO ❌", "capt_cnf_no_btn")
    ]
]


reply_markup_purge = InlineKeyboardMarkup(purge_button)

reply_markup_skip_index = InlineKeyboardMarkup(indexing_skip_button)

reply_markup_skip_purge = InlineKeyboardMarkup(purging_skip_button)

reply_markup_stop = InlineKeyboardMarkup(stop_button)

reply_markup_home = InlineKeyboardMarkup(home_button)

reply_markup_start = InlineKeyboardMarkup(start_button)

reply_markup_terminate = InlineKeyboardMarkup(terminate_btn)

reply_markup_finished = InlineKeyboardMarkup(finished_button)

reply_markup_types_button = InlineKeyboardMarkup(types_button)

reply_markup_close = InlineKeyboardMarkup(close_button)

reply_markup_cap_cnf = InlineKeyboardMarkup(caption_cnf_button)
