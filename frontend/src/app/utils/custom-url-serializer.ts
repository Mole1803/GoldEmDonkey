import {DefaultUrlSerializer, UrlTree} from "@angular/router";

export class CustomUrlSerializer extends DefaultUrlSerializer{
  private _reverseUrl(url: string): string {
    const startIndex = 1;
    const segmentString =
      `(${url.substring(startIndex).split('/').join('//')})`;
    return url.substring(0, startIndex) + segmentString;
  }
  private _beautifyUrl(url: string): string {
    return url
      .replace('(', '')
      .replace(')', '')
      .split('//').join('/');
  }

  override parse(url: string): UrlTree {
    return super.parse(this._reverseUrl(url));
  }

  override serialize(tree: UrlTree): string {
    return this._beautifyUrl(super.serialize(tree));
  }
}
