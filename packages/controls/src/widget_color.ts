// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

import { CoreDescriptionModel } from './widget_core';

import { DescriptionView } from './widget_description';

import { uuid } from './utils';

const named_colors: { [key: string]: string } = {
  aliceblue: '#f0f8ff',
  antiquewhite: '#faebd7',
  aqua: '#00ffff',
  aquamarine: '#7fffd4',
  azure: '#f0ffff',
  beige: '#f5f5dc',
  bisque: '#ffe4c4',
  black: '#000000',
  blanchedalmond: '#ffebcd',
  blue: '#0000ff',
  blueviolet: '#8a2be2',
  brown: '#a52a2a',
  burlywood: '#deb887',
  cadetblue: '#5f9ea0',
  chartreuse: '#7fff00',
  chocolate: '#d2691e',
  coral: '#ff7f50',
  cornflowerblue: '#6495ed',
  cornsilk: '#fff8dc',
  crimson: '#dc143c',
  cyan: '#00ffff',
  darkblue: '#00008b',
  darkcyan: '#008b8b',
  darkgoldenrod: '#b8860b',
  darkgray: '#a9a9a9',
  darkgrey: '#a9a9a9',
  darkgreen: '#006400',
  darkkhaki: '#bdb76b',
  darkmagenta: '#8b008b',
  darkolivegreen: '#556b2f',
  darkorange: '#ff8c00',
  darkorchid: '#9932cc',
  darkred: '#8b0000',
  darksalmon: '#e9967a',
  darkseagreen: '#8fbc8f',
  darkslateblue: '#483d8b',
  darkslategray: '#2f4f4f',
  darkslategrey: '#2f4f4f',
  darkturquoise: '#00ced1',
  darkviolet: '#9400d3',
  deeppink: '#ff1493',
  deepskyblue: '#00bfff',
  dimgray: '#696969',
  dimgrey: '#696969',
  dodgerblue: '#1e90ff',
  firebrick: '#b22222',
  floralwhite: '#fffaf0',
  forestgreen: '#228b22',
  fuchsia: '#ff00ff',
  gainsboro: '#dcdcdc',
  ghostwhite: '#f8f8ff',
  gold: '#ffd700',
  goldenrod: '#daa520',
  gray: '#808080',
  grey: '#808080',
  green: '#008000',
  greenyellow: '#adff2f',
  honeydew: '#f0fff0',
  hotpink: '#ff69b4',
  indianred: '#cd5c5c',
  indigo: '#4b0082',
  ivory: '#fffff0',
  khaki: '#f0e68c',
  lavender: '#e6e6fa',
  lavenderblush: '#fff0f5',
  lawngreen: '#7cfc00',
  lemonchiffon: '#fffacd',
  lightblue: '#add8e6',
  lightcoral: '#f08080',
  lightcyan: '#e0ffff',
  lightgoldenrodyellow: '#fafad2',
  lightgreen: '#90ee90',
  lightgray: '#d3d3d3',
  lightgrey: '#d3d3d3',
  lightpink: '#ffb6c1',
  lightsalmon: '#ffa07a',
  lightseagreen: '#20b2aa',
  lightskyblue: '#87cefa',
  lightslategray: '#778899',
  lightslategrey: '#778899',
  lightsteelblue: '#b0c4de',
  lightyellow: '#ffffe0',
  lime: '#00ff00',
  limegreen: '#32cd32',
  linen: '#faf0e6',
  magenta: '#ff00ff',
  maroon: '#800000',
  mediumaquamarine: '#66cdaa',
  mediumblue: '#0000cd',
  mediumorchid: '#ba55d3',
  mediumpurple: '#9370db',
  mediumseagreen: '#3cb371',
  mediumslateblue: '#7b68ee',
  mediumspringgreen: '#00fa9a',
  mediumturquoise: '#48d1cc',
  mediumvioletred: '#c71585',
  midnightblue: '#191970',
  mintcream: '#f5fffa',
  mistyrose: '#ffe4e1',
  moccasin: '#ffe4b5',
  navajowhite: '#ffdead',
  navy: '#000080',
  oldlace: '#fdf5e6',
  olive: '#808000',
  olivedrab: '#6b8e23',
  orange: '#ffa500',
  orangered: '#ff4500',
  orchid: '#da70d6',
  palegoldenrod: '#eee8aa',
  palegreen: '#98fb98',
  paleturquoise: '#afeeee',
  palevioletred: '#db7093',
  papayawhip: '#ffefd5',
  peachpuff: '#ffdab9',
  peru: '#cd853f',
  pink: '#ffc0cb',
  plum: '#dda0dd',
  powderblue: '#b0e0e6',
  purple: '#800080',
  red: '#ff0000',
  rosybrown: '#bc8f8f',
  royalblue: '#4169e1',
  saddlebrown: '#8b4513',
  salmon: '#fa8072',
  sandybrown: '#f4a460',
  seagreen: '#2e8b57',
  seashell: '#fff5ee',
  sienna: '#a0522d',
  silver: '#c0c0c0',
  skyblue: '#87ceeb',
  slateblue: '#6a5acd',
  slategray: '#708090',
  slategrey: '#708090',
  snow: '#fffafa',
  springgreen: '#00ff7f',
  steelblue: '#4682b4',
  tan: '#d2b48c',
  teal: '#008080',
  thistle: '#d8bfd8',
  tomato: '#ff6347',
  turquoise: '#40e0d0',
  violet: '#ee82ee',
  wheat: '#f5deb3',
  white: '#ffffff',
  whitesmoke: '#f5f5f5',
  yellow: '#ffff00',
  yellowgreen: '#9acd32'
};

export class ColorPickerModel extends CoreDescriptionModel {
  defaults(): Backbone.ObjectHash {
    return {
      ...super.defaults(),
      value: 'black',
      concise: false,
      _model_name: 'ColorPickerModel',
      _view_name: 'ColorPickerView'
    };
  }
}

export class ColorPickerView extends DescriptionView {
  render(): void {
    super.render();
    this.el.classList.add('jupyter-widgets');
    this.el.classList.add('widget-inline-hbox');
    this.el.classList.add('widget-colorpicker');

    this._color_container = document.createElement('div');
    this._color_container.className =
      'widget-inline-hbox widget-colorpicker-input';
    this.el.appendChild(this._color_container);

    this._textbox = document.createElement('input');
    this._textbox.setAttribute('type', 'text');
    this._textbox.id = this.label.htmlFor = uuid();

    this._color_container.appendChild(this._textbox);
    this._textbox.value = this.model.get('value');

    this._colorpicker = document.createElement('input');
    this._colorpicker.setAttribute('type', 'color');
    this._color_container.appendChild(this._colorpicker);

    this.listenTo(this.model, 'change:value', this._update_value);
    this.listenTo(this.model, 'change:concise', this._update_concise);

    this._update_concise();
    this._update_value();
    this.update();
  }

  /**
   * Update the contents of this view
   *
   * Called when the model is changed. The model may have been
   * changed by another view or by a state update from the back-end.
   */
  update(options?: any): void {
    if (options === undefined || options.updated_view != this) {
      const disabled = this.model.get('disabled');
      this._textbox.disabled = disabled;
      this._colorpicker.disabled = disabled;
    }
    return super.update();
  }

  events(): { [e: string]: string } {
    // Typescript doesn't understand that these functions are called, so we
    // specifically use them here so it knows they are being used.
    void this._picker_change;
    void this._text_change;
    return {
      'change [type="color"]': '_picker_change',
      'change [type="text"]': '_text_change'
    };
  }

  private _update_value(): void {
    const value = this.model.get('value');
    this._colorpicker.value = color2hex(value);
    this._textbox.value = value;
  }

  private _update_concise(): void {
    const concise = this.model.get('concise');
    if (concise) {
      this.el.classList.add('concise');
      this._textbox.style.display = 'none';
    } else {
      this.el.classList.remove('concise');
      this._textbox.style.display = '';
    }
  }

  private _picker_change(): void {
    this.model.set('value', this._colorpicker.value);
    this.touch();
  }

  private _text_change(): void {
    const value = this._validate_color(
      this._textbox.value,
      this.model.get('value')
    );
    this.model.set('value', value);
    this.touch();
  }

  private _validate_color(color: string, fallback: any): any {
    return color.match(/#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$/) ||
      named_colors[color.toLowerCase()]
      ? color
      : fallback;
  }

  private _color_container: HTMLDivElement;
  private _textbox: HTMLInputElement;
  private _colorpicker: HTMLInputElement;
}

/*
 * From a valid html color (named color, 6-digits or 3-digits hex format)
 * return a 6-digits hexadecimal color #rrggbb.
 */
function color2hex(color: string): string {
  return named_colors[color.toLowerCase()] || rgb3_to_rgb6(color);
}

function rgb3_to_rgb6(rgb: string): string {
  if (rgb.length === 7) {
    return rgb;
  } else {
    return (
      '#' +
      rgb.charAt(1) +
      rgb.charAt(1) +
      rgb.charAt(2) +
      rgb.charAt(2) +
      rgb.charAt(3) +
      rgb.charAt(3)
    );
  }
}
